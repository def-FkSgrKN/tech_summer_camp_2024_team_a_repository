"use client";

import { useEffect, useRef } from "react";

interface CameraPageProps {
  session: any;
}

const CameraPage: React.FC<CameraPageProps> = ({ session }) => {
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
      if (videoRef.current && videoRef.current.srcObject) {
        (videoRef.current.srcObject as MediaStream)
          .getTracks()
          .forEach((track) => track.stop());
      }
    };
  }, []);

  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext("2d");
      if (context) {
        context.drawImage(
          videoRef.current,
          0,
          0,
          canvasRef.current.width,
          canvasRef.current.height
        );
        const base64Image = canvasRef.current.toDataURL("image/png");
        sendToServer(base64Image);
      }
    }
  };

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
          Authorization: `Bearer ${session.accessToken}`,
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
    const intervalId = setInterval(captureImage, 5000);

    return () => clearInterval(intervalId);
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
};

export default CameraPage;
