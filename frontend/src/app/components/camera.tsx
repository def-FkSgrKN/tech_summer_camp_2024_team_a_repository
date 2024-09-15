"use client";

import { useEffect, useRef } from "react";
import { useSession } from "next-auth/react";

export default function CameraPage() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const { data: session } = useSession(); // セッションからJWTトークンを取得

  useEffect(() => {
    // カメラストリームを取得する
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

    // カメラストリームを停止する
    return () => {
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
        sendToServer(base64Image);
      }
    }
  };

  // サーバーに画像を送信
  const sendToServer = async (base64Image: string) => {
    if (!session || !session.accessToken) {
      console.error("JWTトークンが見つかりません");
      return;
    }

    try {
      const response = await fetch("http://localhost:8080/capture_img", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session.accessToken}`, // JWTトークンをヘッダーに追加
        },
        body: JSON.stringify({ image: base64Image }),
      });
      const result = await response.json();
      console.log("サーバーの応答:", result);
    } catch (err) {
      console.error("画像送信エラー:", err);
    }
  };

  useEffect(() => {
    // 5秒ごとに画像をキャプチャしてサーバーに送信
    const intervalId = setInterval(captureImage, 5000);

    return () => clearInterval(intervalId); // コンポーネントのアンマウント時にインターバルをクリア
  }, []);

  return (
    <div>
      <video
        ref={videoRef}
        autoPlay
        playsInline
        className="border-2 border-black rounded-lg"
      />
      <canvas
        ref={canvasRef}
        width="640"
        height="480"
        className="hidden"
      ></canvas>
    </div>
  );
}
