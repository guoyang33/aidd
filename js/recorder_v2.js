/*
 * V2:
    * 1. 加入錄音秒數顯示
    * 2. 加入聲音能量顯示
    * 3. 加入上傳功能
    * 4. 錄音按鈕改為按一下開始錄音，再按一下結束錄音
    * 5. 結束錄音後會進行初步判斷，若判斷為有效錄音長度(5-10秒)，則會上傳至伺服器
 */

var record_button = document.querySelector('.record-btn'),
    record_player = document.querySelector('.record-player'),
    record_msg_box = document.querySelector('.record-msg'),
    submit_button = document.querySelector('.submit-btn'),
    lang = {
        'mic_error': '您的裝置不支援錄音功能',
        'press_to_start': '點擊上方按鈕開始錄音',
        'play_record_available': '點擊下方按鈕試聽錄音與送出',
    },
    time,
    record_time,
    record_time_ms,
    record_time_s,
    record_time_m,
    record_timer;

if (navigator.mediaDevices === undefined) {
    navigator.mediaDevices = {};
}

if (navigator.mediaDevices.getUserMedia === undefined) {
    navigator.mediaDevices.getUserMedia = function (constraints) {
        // 首先，如果有getUserMedia的話，就請它包含getUserMedia
        var getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

        // 一個Promise，如果有getUserMedia的話，就請它包含getUserMedia，否則就拒絕
        if (!getUserMedia) {
            return Promise.reject(
                new Error("getUserMedia is not implemented in this browser")
            );
        }

        return new Promise(function (resolve, reject) {
            getUserMedia.call(navigator, constraints, resolve, reject);
        });
    };
}

if (navigator.mediaDevices.getUserMedia) {
    var btn_status = 'inactive',
        mediaRecorder,
        chunks = [],
        type = {
            'type': 'audio/mp3'
        },
        analys,
        blob;

    record_button.onclick = function () {
        if (btn_status == 'inactive') {
            start();
        } else if (btn_status == 'recording') {
            stop();
        }
    }
    
    function start() {
        navigator.mediaDevices.getUserMedia({ 'audio': true }).then(
            function (stream) {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();

                record_button.classList.add("recording");
                btn_status = 'recording';
                record_player.classList.add('d-none');
                submit_button.classList.add('d-none');
                record_msg_box.classList.remove('d-none');

                time = new Date().getTime();

                record_timer = setInterval(function () {
                    record_time = new Date().getTime() - time;
                    record_time_ms = record_time % 1000;
                    record_time_s = Math.floor(record_time / 1000) % 60;
                    record_time_m = Math.floor(record_time / 60000) % 60;
                    // 顯示錄音時間
                    record_msg_box.innerHTML = '正在錄音...<br>' + String(record_time_m).padStart(2, "0") + ":" + String(record_time_s).padStart(2, "0") + "." + String(record_time_ms).padStart(3, "0");
                    if (record_time > 10*1000) {
                        stop();
                        alert('錄音時間達10秒，已自動停止錄音，請按下方按鈕上傳錄音檔案');
                    }
                }, 50);

                mediaRecorder.ondataavailable = function (e) {
                    chunks.push(e.data);
                }

                mediaRecorder.onstop = function () {
                    stream.getTracks().forEach(function (track) {
                        track.stop();
                    });

                    blob = new Blob(chunks, type);
                    chunks = [];

                    // 改變HTML元素屬性
                    if (record_time < 5*1000) {
                        record_msg_box.textContent = '錄音時間過短，請麻煩您重新錄音';
                        record_msg_box.classList.remove('d-none');
                    } else {
                        record_player.src = URL.createObjectURL(blob);
                        record_player.classList.remove('d-none');
                        submit_button.classList.remove('d-none');
                        record_msg_box.innerHTML = lang['play_record_available'];
                        record_msg_box.classList.remove('d-none');
                    }
                }
            }
        ).catch(function (err) {
            console.log(err);
            record_button.disabled = true;
        });
    }

    function stop() {
        mediaRecorder.stop();
        clearInterval(record_timer);
        record_button.classList.remove("recording");
        record_msg_box.classList.add('d-none');
        btn_status = 'inactive';
    }

    // Initial state
    record_msg_box.textContent = lang['press_to_start'];
} else {
    record_button.disabled = true;
    record_msg_box.textContent = lang['mic_error'];
}

// 上傳錄音
function upload_record() {
    var fd = new FormData();
    fd.append('audio_data', blob, 'test.mp3');
    $.ajax({
        type: 'post',
        url: 'audio_target_demo.php',
        data: fd,
        processData: false,
        contentType: false
    }).done(function (data) {
        console.log(data);
    })
}