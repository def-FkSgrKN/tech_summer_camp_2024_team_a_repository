"use client";
import { useEffect, useRef } from "react";

export default function CameraPage() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const getCameraStream = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("カメラへのアクセスエラー: ", err);
      }
    };

    getCameraStream();

    return () => {
      // コンポーネントがアンマウントされた時にカメラストリームを停止
      if (videoRef.current && videoRef.current.srcObject) {
        (videoRef.current.srcObject as MediaStream)
          .getTracks()
          .forEach((track) => track.stop());
      }
    };
  }, []);

  // 画像をキャプチャしてサーバーに送信
  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext("2d");
      if (context) {
        // canvasにビデオフレームを描画
        context.drawImage(
          videoRef.current,
          0,
          0,
          canvasRef.current.width,
          canvasRef.current.height
        );
        // canvasからbase64形式の画像を取得
        const base64Image = canvasRef.current.toDataURL("image/png");
        // base64形式の画像をサーバーに送信
        // sendToServer(base64Image);
        console.log(base64Image);
      }
    }
  };

  // サーバーに画像を送信
  const sendToServer = async (base64Image: string) => {
    try {
      const response = await fetch("http://localhost:80800/capture_img", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image: base64Image }),
      });
      const result = await response.json();
      console.log("サーバーの応答:", result);
    } catch (err) {
      console.error("画像送信エラー:", err);
    }
  };

  return (
    <div>
      <video
        ref={videoRef}
        autoPlay
        playsInline
        className=" border-2 border-black rounded-lg"
      />
      <canvas
        ref={canvasRef}
        width="640"
        height="480"
        className="hidden"
      ></canvas>
      <div className="flex justify-center ">
        <button
          onClick={captureImage}
          className="px-4 mt-5 py-2 bg-blue-500 text-white rounded-lg"
        >
          Capture Image
        </button>
      </div>
    </div>
  );
}
