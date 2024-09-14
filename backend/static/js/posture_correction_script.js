var video = document.getElementById('video');
// getUserMedia()でカメラ映像の取得
var media = navigator.mediaDevices.getUserMedia({ video: true });
//リアルタイム再生（ストリーミング）を行うためにビデオタグに流し込む
media.then((stream) => {
    video.srcObject = stream;
});

var canvas = document.getElementById('canvas');
canvas.setAttribute('width', video.width);
canvas.setAttribute('height', video.height);

video.addEventListener(
    'timeupdate',
    function () {
        var context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, video.width, video.height);
    },
    true
);

// スペースキー押下時にキャプチャ取得を実行するリスナーを設定
/*
document.addEventListener('keydown', (event) => {
    alert("キーが押されました")

    var keyName = event.key;
    if (keyName === ' ') {
        console.log(`keydown: SpaceKey`);
        context = canvas.getContext('2d');
        // 取得したbase64データのヘッドを取り除く
        var img_base64 = canvas.toDataURL('image/jpeg').replace(/^.*,/, '')
        captureImg(img_base64);
    }
});
*/

window.addEventListener('DOMContentLoaded', function(){
  
    // 1秒ごとに実行
    setInterval(() => {
        context = canvas.getContext('2d');
        // 取得したbase64データのヘッドを取り除く
        var img_base64 = canvas.toDataURL('image/jpeg').replace(/^.*,/, '')
        captureImg(img_base64);
    }, 500);
  
    
    
  
});


var xhr = new XMLHttpRequest();

// キャプチャ画像データ(base64)をPOST
function captureImg(img_base64) {
    const body = new FormData();
    body.append('img', img_base64);
    xhr.open('POST', '/capture_img', true);
    xhr.onload = () => {
        console.log(xhr.responseText)
    };
    xhr.send(body);
}