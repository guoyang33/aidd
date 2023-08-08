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
from datetime import datetime

ROOT_DIR = Path(__file__).parents[0]  # Python腳本根目錄
# Append script/ path
sys.path.append(ROOT_DIR.__str__())
# Import model class
from CNN1D_MDPI_5s import CNN1D_MDPI_5
# BEST PTH Path
BEST_PTH_PATH = ROOT_DIR / 'pth/best.pth'
# MySQL Login Info
MYSQL_LOGIN_INFO = {
    'host': 'localhost',
    'user': 'aidd',
    'password': 'x6aROQwW.i8Kb@D_',
    'db': 'aidd',
}

def main():
    # 載入模型
    model = torch.load(Path('pth', 'best.pth'), map_location=torch.device('cpu'))
    model.to('cuda')
    model.eval()

    # 音檔路徑
    sound_record_upload_dir = Path(__file__).parents[1] / 'sound_record_upload'

    # 資料庫連線
    conn = pymysql.Connection(host=MYSQL_LOGIN_INFO['host'], user=MYSQL_LOGIN_INFO['user'], password=MYSQL_LOGIN_INFO['password'], db=MYSQL_LOGIN_INFO['db'], charset='utf8')
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
                

    # exit()

root_dir = Path(__file__).parents[0]
sys.path.append(root_dir.__str__())
from CNN1D_MDPI_5s import CNN1D_MDPI_5

pth_path = root_dir / 'pth/best.pth'
# sys.path.append(root_dir.__str__())

if __name__ == '__main__':
    main()
    model = torch.load(pth_path)
    print(model)
    # print(root_dir)

    # print(*os.listdir(root_dir))

    torch
    # parser = argparse.ArgumentParser(description='')
    # parser.add_argument('--model', type=str, default='', help='model path')
    # parser.add_argument('--sound', type=str, default='', help='audio path')