import cv2
import mediapipe as mp

# MediaPipe Pose モジュールを初期化
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

print("画像パスを入力してください")
image_path = input("画像パス:")

# 画像を読み込む
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# ポーズトラッキングを実行
results = pose.process(image_rgb)

# ランドマークが検出されたら
if results.pose_landmarks:
    # 各ランドマークに番号を付けて画像に描画
    for idx, landmark in enumerate(results.pose_landmarks.landmark):
        # ランドマークの位置を画像サイズに合わせてスケーリング
        height, width, _ = image.shape
        x = int(landmark.x * width)
        y = int(landmark.y * height)

        # ランドマーク番号を描画
        cv2.putText(image, str(idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # ランドマークと接続線を描画
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

# 画像を表示
cv2.imshow('Pose Tracking', image)
cv2.imwrite(image_path.replace(".png", "") + "point_num.png", image)
cv2.waitKey(0)
cv2.destroyAllWindows()