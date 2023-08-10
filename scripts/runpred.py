'''
runpred.py
使用輸入的音檔進行失智症預測
'''
import pymysql
import os
import sys
import torch
import librosa
from pathlib import Path
import time

ROOT_DIR = Path(__file__).parents[0]  # Python腳本根目錄
# Append script/ path
sys.path.append(ROOT_DIR.__str__())
# Import model class
from CNN1D_MDPI_5s import CNN1D_MDPI_5
from get_transform import get_transform
# BEST PTH Path
BEST_PTH_PATH = ROOT_DIR / 'pth/best.pth'
# print(BEST_PTH_PATH)
# exit()
# MySQL Login Info
MYSQL_LOGIN_INFO = {
    'host': 'localhost',
    'user': 'aidd',
    'password': 'x6aROQwW.i8Kb@D_',
    'db': 'aidd',
}

def main():
    # 載入模型
    model = torch.load(BEST_PTH_PATH, map_location=torch.device('cpu'))
    model.to('cuda')
    model.eval()

    # 音檔路徑
    sound_record_upload_dir = Path(__file__).parents[1] / 'sound_record_upload'

    # 載入轉換函式
    transform = get_transform()


    while True:
        # 資料庫連線
        conn = pymysql.Connection(host=MYSQL_LOGIN_INFO['host'], user=MYSQL_LOGIN_INFO['user'], password=MYSQL_LOGIN_INFO['password'], db=MYSQL_LOGIN_INFO['db'], charset='utf8')
        # 取得資料庫中尚未預測的資料
        print('Getting data from database...')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM `test_record` WHERE `predict_result` IS NULL")
        result = cursor.fetchall()
        cursor.close()
        if len(result) == 0:
            print('No data to predict.')
        else:
            for row in result:
                tr_id = row['id']
                print(f'ID: {tr_id}')
                sound_file_path = f'{sound_record_upload_dir}/{tr_id}.mp3'
                if not os.path.exists(sound_file_path):
                    print(f'File not found: {sound_file_path}')
                    # 從資料庫刪除
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM `test_record` WHERE `id` = {tr_id}")
                    conn.commit()
                    cursor.close()
                    continue
                else:
                    print('Predicting...')
                    # 讀取音檔
                    x, sr = librosa.load(sound_file_path, sr=44100, mono=True, duration=5)
                    x_processed = transform(x)
                    x_toDevice = x_processed.to('cuda')
                    try:
                        y_pred = int(model(x_toDevice).argmax(1).cpu().numpy()[0])
                        print(f'Predict result: {y_pred}')
                    except ValueError as e:
                        print(e)
                    
                    # 更新資料庫
                    print('Updating database...')
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE `test_record` SET `predict_result`='{y_pred}', `result_time`=CURRENT_TIMESTAMP WHERE `id` = {tr_id}")
                    conn.commit()
                    cursor.close()
                    print('Done.')

                    # 刪除音檔
                    # os.remove(sound_file_path)
                    # print('File deleted.')

        print('Sleeping...')
        # 休息一段時間
        time.sleep(5)


if __name__ == '__main__':
    main()