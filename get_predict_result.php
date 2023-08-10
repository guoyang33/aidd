<?php
/*
 * get_predict_result.php
 * 取得預測結果
 */

// 時區
date_default_timezone_set('Asia/Taipei');

header("Content-Type:application/json; charset=utf-8");

require_once 'connect_db.php';
require_once 'error_info.php';

$response_status = null;
$response_error_msg = null;
$response_contents = array();

$tr_id = $_POST['tr_id'];

$sth = $dbh->prepare("SELECT * FROM `test_record` WHERE `id` = :tr_id;");
$sth->bindParam(':tr_id', $tr_id);
$sth->execute();
$test_record = $sth->fetch(PDO::FETCH_ASSOC);

if ($test_record === false) {
    $response_status = 'ERROR_DB_NO_RECORD';
} else {
    $response_status = 'OK';
    if ($test_record['predict_result'] === null) {
        $response_contents['predict_finish'] = false;
        $response_contents['predict_result'] = null;
    } else {
        $response_contents['predict_finish'] = true;
        if ($test_record['predict_result'] == 1) {
            $response_contents['predict_result'] = '預測為失智症';
        } else {
            $response_contents['predict_result'] = '預測為健康';
        }
    }
}

# 回傳結果
if (in_array($response_status, array_keys($ERROR_MSG))) {
    $response_error_msg = $ERROR_MSG[$response_status];
}
echo json_encode(array(
    'headers' => array(
        'status' => $response_status,
        'error_msg' => $response_error_msg
    ),
    'contents' => $response_contents
));

?>