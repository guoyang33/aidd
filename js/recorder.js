const recordBtn = document.querySelector(".record-btn");
const player = document.querySelector(".audio-player");

if (navigator.mediaDevices.getUserMedia) {
  var chunks = [];
  const constraints = { audio: true };
  navigator.mediaDevices.getUserMedia(constraints).then(
    stream => {
      console.log("授权成功！");

      const mediaRecorder = new MediaRecorder(stream);

      recordBtn.onclick = () => {
        if (mediaRecorder.state === "recording") {
          mediaRecorder.stop();
          recordBtn.textContent = "Start";
          console.log("录音结束");
        } else {
          mediaRecorder.start();
          console.log("录音中...");
          recordBtn.textContent = "Stop";
        }
        console.log("录音器状态：", mediaRecorder.state);
      };

      mediaRecorder.ondataavailable = e => {
        chunks.push(e.data);
      };

      mediaRecorder.onstop = e => {
        var blob = new Blob(chunks, { type: "audio/mp3" });
        // var blob = new Blob(chunks, { type: "audio/ogg; codecs=opus" });
        chunks = [];
        var audioURL = window.URL.createObjectURL(blob);
        player.src = audioURL;

        // 上傳 added by CYouLiao 2023/06/24
        var fd = new FormData();
        fd.append('audio_data', blob, 'test.mp3');
        $.ajax({
            type: 'post',
            url: 'audio_target_demo.php',
            data: fd,
            processData: false,
            contentType: false
        }).done(function(data) {
            console.log(data);
        })
      };
    },
    () => {
      console.error("授权失败！");
    }
  );
} else {
  console.error("浏览器不支持 getUserMedia");
}