"use client";

import { useEffect, useRef, useState } from "react";

export default function Home() {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const landmarkBuffer = useRef<number[][]>([]);
  const [loaded, setLoaded] = useState(false);

  function flattenLandmarks(results: any): number[] {
    const right =
      results.rightHandLandmarks ?? Array(21).fill({ x: 0, y: 0, z: 0 });
    const left =
      results.leftHandLandmarks ?? Array(21).fill({ x: 0, y: 0, z: 0 });

    const points = [...right, ...left];
    return points.flatMap((p) => [p.x, p.y, p.z]);
  }

  useEffect(() => {
    const loadScripts = async () => {
      const loadScript = (src: string): Promise<void> =>
        new Promise((resolve) => {
          const script = document.createElement("script");
          script.src = src;
          script.async = true;
          script.onload = () => resolve();
          document.body.appendChild(script);
        });

      // 必要なCDNスクリプトを読み込む
      await loadScript(
        "https://cdn.jsdelivr.net/npm/@mediapipe/holistic/holistic.js"
      );
      await loadScript(
        "https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js"
      );
      await loadScript(
        "https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"
      );

      setLoaded(true);
    };

    loadScripts();
  }, []);

  useEffect(() => {
    if (!loaded) return;

    const holistic = new (window as any).Holistic({
      locateFile: (file: string) =>
        `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`,
    });

    holistic.setOptions({
      modelComplexity: 1,
      smoothLandmarks: true,
      enableSegmentation: false,
      refineFaceLandmarks: true,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });

    holistic.onResults((results: any) => {
      const canvasCtx = canvasRef.current?.getContext("2d");
      if (!canvasCtx || !results.image) return;

      canvasCtx.save();
      canvasCtx.clearRect(0, 0, 640, 480);
      canvasCtx.drawImage(results.image, 0, 0, 640, 480);

      const drawConnectors = (window as any).drawConnectors;
      const drawLandmarks = (window as any).drawLandmarks;

      if (results.rightHandLandmarks) {
        drawConnectors(
          canvasCtx,
          results.rightHandLandmarks,
          (window as any).HAND_CONNECTIONS,
          {
            color: "#00FF00",
            lineWidth: 2,
          }
        );
        drawLandmarks(canvasCtx, results.rightHandLandmarks, {
          color: "#FF0000",
          lineWidth: 1,
        });
      }

      if (results.leftHandLandmarks) {
        drawConnectors(
          canvasCtx,
          results.leftHandLandmarks,
          (window as any).HAND_CONNECTIONS,
          {
            color: "#0000FF",
            lineWidth: 2,
          }
        );
        drawLandmarks(canvasCtx, results.leftHandLandmarks, {
          color: "#FFFF00",
          lineWidth: 1,
        });
      }

      const frameData = flattenLandmarks(results);
      landmarkBuffer.current.push(frameData);

      if (landmarkBuffer.current.length >= 30) {
        const payload = { sequence: landmarkBuffer.current };

        fetch("http://localhost:8000/predict", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        })
          .then((res) => res.json())
          .then((data) => {
            console.log("予測ラベル:", data.label, "信頼度:", data.confidence);
          })
          .catch((err) => {
            console.error("推論リクエスト失敗:", err);
          });

        landmarkBuffer.current = []; // バッファリセット
      }
      canvasCtx.restore();
    });

    if (videoRef.current) {
      // ✅ camera_utils.js 読み込み後に使えるようになる
      const Camera = (window as any).Camera;
      const camera = new Camera(videoRef.current, {
        onFrame: async () => {
          await holistic.send({ image: videoRef.current! });
        },
        width: 640,
        height: 480,
      });
      camera.start();
    }
  }, [loaded]);

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <video
        ref={videoRef}
        style={{ display: "none" }}
        width="640"
        height="480"
        playsInline
      />
      <canvas
        ref={canvasRef}
        width="640"
        height="480"
        style={{ border: "1px solid black" }}
      />
    </div>
  );
}
