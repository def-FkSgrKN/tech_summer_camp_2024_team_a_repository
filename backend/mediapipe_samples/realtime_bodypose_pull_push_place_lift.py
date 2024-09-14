import cv2
import mediapipe as mp
import numpy as np

# MediaPipe Poseの初期化
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# カメラの初期化
cap = cv2.VideoCapture(0)

# 過去の手の位置を記録するリスト
previous_hand_position = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # BGRをRGBに変換
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # MediaPipeでポーズを検出
    results = pose.process(image_rgb)
    
    if results.pose_landmarks:
        # ランドマークを取得（ここでは右手の座標を使用）
        landmarks = results.pose_landmarks.landmark
        right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

        # 手のx, y, z座標を取得
        current_hand_position = np.array([right_hand.x, right_hand.y, right_hand.z])

        if previous_hand_position is not None:
            # 手の移動ベクトルを計算
            movement_vector = current_hand_position - previous_hand_position
            movement_direction = np.sign(movement_vector)

            # 動作の分類
            if movement_direction[1] < 0 and abs(movement_vector[1]) > 0.01:  # 手が上に移動している場合
                action = "Lifting"
            elif movement_direction[1] > 0 and abs(movement_vector[1]) > 0.01:  # 手が下に移動している場合
                action = "Placing"
            elif movement_direction[2] > 0 and abs(movement_vector[2]) > 0.01:  # 手が前方に移動している場合
                action = "Pushing"
            elif movement_direction[2] < 0 and abs(movement_vector[2]) > 0.01:  # 手が後方に移動している場合
                action = "Pulling"
            else:
                action = "Idle"
        else:
            action = "Idle"

        # 動作を画面に表示
        cv2.putText(frame, f"Action: {action}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # 前回の手の位置を更新
        previous_hand_position = current_hand_position

    # ポーズを描画
    mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    # 結果を表示
    cv2.imshow('Action Detection', frame)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()