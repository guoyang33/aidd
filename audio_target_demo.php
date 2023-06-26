<?php

/*
 * 一個接收資料的backend，並將資料寫入本地目錄以及MySQL資料庫
 * 最終回傳一個JSON格式的資料，以適配前端AJAX調用
 */

// 設定時區
date_default_timezone_set('Asia/Taipei');

// 取得HTTP POST資料

// $fname = $_POST['fname'];
// $blob = $_POST['blob'];

print_r($_FILES);

// 讀取音檔
$sound_file = $_FILES['audio_data'];
$temp_file = $sound_file['tmp_name'];
// $target_file = './'.$sound_file['name'];
$target_file = './test2.ogg';
move_uploaded_file($temp_file, $target_file);

?>