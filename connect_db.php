<?php

// 設定時區
date_default_timezone_set('Asia/Taipei');

// require_once 'MyPDO.php';

// 以下是 PDO 的宣告 $dbh 就是 資料庫 的database handle

$driver = 'mysql';
$host = 'localhost';
$port = ';port=3306';
$dbname = 'aidd';
$dsn = "{$driver}:host={$host}{$port};dbname={$dbname}";

$username = 'aidd';
$password = 'x6aROQwW.i8Kb@D_';     // remote
// $password = 'root1234';          // local
$dbh = new PDO($dsn, $username, $password);

$dbh->exec("SET CHARACTER SET 'UTF8';");
$dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

// print_r($dbh->errorInfo());      // Array ( [0] => 00000 [1] => [2] => )

// 常數

// 使用時間格式化: 秒數 => HH:MM:SS
function time_beautifier($seconds) {
    $beautiful_time =   str_pad(floor($seconds/3600), 2, '0', STR_PAD_LEFT).':'.
                        str_pad(floor($seconds/60)%60, 2, '0', STR_PAD_LEFT).':'.
                        str_pad($seconds%60, 2, '0', STR_PAD_LEFT);
                        return $beautiful_time;
}

// 產生長度 6 的英數亂碼，當密碼用
function randomPassword() {
    $alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
    $pass = array(); //remember to declare $pass as an array
    $alphaLength = strlen($alphabet) - 1; //put the length -1 in cache
    for ($i = 0; $i < 6; $i++) {
        $n = rand(0, $alphaLength);
        $pass[] = $alphabet[$n];
    }
    return implode($pass); //turn the array into a string
}

// try
// {
// 	$dbh = new MyPDO();
// 	$dbh->exec("SET CHARACTER SET 'UTF8';");
// 	$dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
// }
// catch (Exception $e)
// {
// 	echo '
// 		<center style="padding-top:15%;">
// 		<strong><font color="#FF0000" size="+1">未知錯誤發生，請聯絡系統管理員。</font></strong><br><br>
// 		請點 <a href="./index.php"><strong><font size="+1">這裡</font></strong></a> 以返回系統首頁。
// 	';
// 	die();
// }
// catch (PDOException $e)
// {
// 	echo '
// 		<center style="padding-top:15%;">
// 		<strong><font color="#FF0000" size="+1">資料庫連線失敗，請聯絡系統管理員。</font></strong><br><br>
// 		請點 <a href="./index.php"><strong><font size="+1">這裡</font></strong></a> 以返回系統首頁。
// 	';
// 	die();
// }
?>