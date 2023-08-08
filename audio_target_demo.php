<?php

/*
 * 一個接收資料的backend，並將資料寫入本地目錄以及MySQL資料庫的範例
 */

header("Content-Type:application/json; charset=utf-8");

// 設定時區
date_default_timezone_set('Asia/Taipei');

$RECORD_FILE_KEY_NAME = 'sound_record';
$RECORD_FILE_UPLOAD_DIR = './sound_record_upload';

// 取得HTTP POST資料
if (!in_array($_SERVER['REQUEST_METHOD'], ['POST'])) {
    echo json_encode(['status' => 'error', 'message' => 'Method not allowed']);
    exit;
} else {
    if (!in_array($RECORD_FILE_KEY_NAME, array_keys($_FILES))) {
        echo json_encode(['status' => 'error', 'message' => 'No file uploaded']);
        exit;
    } else {
        // 寫入資料庫
        require_once 'connect_db.php';

        $sth = $dbh->prepare("INSERT INTO `test_record` (`id`, `test_time`) VALUES (NULL, CURRENT_TIMESTAMP);");
        $sth->execute();
        $last_id = $dbh->lastInsertId();
        if ($last_id < 1) {
            echo json_encode(['status' => 'error', 'message' => 'Database error']);
            exit;
        } else {
            // 移動檔案
            $file_sound_record = $_FILES[$RECORD_FILE_KEY_NAME];
            $file_tmp_name = $file_sound_record['tmp_name'];
            $target_file_path = $RECORD_FILE_UPLOAD_DIR.'/'.$last_id.'.mp3';
            if (!move_uploaded_file($file_tmp_name, $target_file_path)) {
                echo json_encode(['status' => 'error', 'message' => 'File move error']);
                exit;
            } else {
                echo json_encode(['status' => 'success', 'message' => 'File uploaded']);
                exit;
            }
        }
    }
}

// $fname = $_POST['fname'];
// $blob = $_POST['blob'];

// echo json_encode($_FILES);

// 讀取音檔
// $file_sound_record = $_FILES['sound_record'];
// $fname = pathinfo($sound_file['full_path']);
// $tmp_name = pathinfo($sound_file['tmp_name']);
// $temp_file = $sound_file['tmp_name'];
// $target_file = './sound_tmp/'.$tmp_name['filename'].'.'.$fname['extension'];
// $target_file = './'.$sound_file['name'];
// $target_file = './test2.ogg';
// move_uploaded_file($temp_file, $target_file);

// exec("");

// 清除暫存檔
// unlink($temp_file);

?>