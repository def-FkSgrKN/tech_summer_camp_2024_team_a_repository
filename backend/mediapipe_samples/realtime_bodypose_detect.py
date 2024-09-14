import cv2
import mediapipe as mp
import os

#attached_ssd_drive_mediapipe_model_path = "D:\ユーザーバックアップ\sfSogoFurukawa\機械学習モデル_pkg\MediaPipe_Models"
# キャッシュディレクトリを外付けSSDに設定
#os.environ['XDG_CACHE_HOME'] = attached_ssd_drive_mediapipe_model_path

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
 
# Webカメラから入力
cap = cv2.VideoCapture(0)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    #print("results.pose_landmarks.landmark=" + str(results.pose_landmarks.landmark))
    try:
      print("len(results.pose_landmarks.landmark)=" + str(len(results.pose_landmarks.landmark)))

    except:
      print("例外resultがNone")
 
    # 検出されたポーズの骨格をカメラ画像に重ねて描画
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()