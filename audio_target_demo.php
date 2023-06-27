<?php

/*
 * 一個接收資料的backend，並將資料寫入本地目錄以及MySQL資料庫的範例
 */

// 設定時區
date_default_timezone_set('Asia/Taipei');

// 取得HTTP POST資料

// $fname = $_POST['fname'];
// $blob = $_POST['blob'];

print_r($_FILES);

// 讀取音檔
$sound_file = $_FILES['audio_data'];
$fname = pathinfo($sound_file['full_path']);
$tmp_name = pathinfo($sound_file['tmp_name']);
$temp_file = $sound_file['tmp_name'];
$target_file = './sound_tmp/'.$tmp_name['filename'].'.'.$fname['extension'];
// $target_file = './'.$sound_file['name'];
// $target_file = './test2.ogg';
move_uploaded_file($temp_file, $target_file);

// 清除暫存檔
// unlink($temp_file);

?>