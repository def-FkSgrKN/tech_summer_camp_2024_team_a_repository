import cv2
import mediapipe as mp

# MediaPipe Pose モジュールの初期化
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# カメラからの映像をキャプチャ
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # BGRからRGBに変換
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # MediaPipeでポーズを推定
    results = pose.process(image_rgb)
    
    if results.pose_landmarks:
        # 肩と腰のランドマーク取得
        landmarks = results.pose_landmarks.landmark
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        
        print("right_shoulder.x=" +str(right_shoulder.x))
        print("right_shoulder.z=" + str(right_shoulder.z))
        print("\n")

        print("left_shoulder.x=" + str(left_shoulder.x))
        print("left_shoulder.z=" + str(left_shoulder.z))
        print("\n")

        print("\n")

        # 肩のx座標で向きを推定
        if right_shoulder.x > left_shoulder.x:
            direction = "Front facing"
        elif right_shoulder.x < left_shoulder.x:
            direction = "Back facing"
        else:
            direction = "Facing forward"
        
        # 結果を画面に表示
        cv2.putText(frame, f"Direction: {direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # ランドマークと接続線を描画
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    # 結果を表示
    cv2.imshow('Pose Direction', frame)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()