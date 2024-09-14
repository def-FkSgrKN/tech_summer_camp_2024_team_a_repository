import base64
import numpy as np
import cv2

from prevents_hunchback_mediapipe_lib import set_video_capture_in_python, main_detect_prevent_hunchback

class img_process_service:

    def __init__(self):
        self.mp_pose, self.pose = set_video_capture_in_python()
        

    #保存しない場合 画像データのみを取得して処理
    def detect_hunchback_from_img(self, img_base64):
        #binary <- string base64
        img_binary = base64.b64decode(img_base64)
        #jpg <- binary
        img_jpg=np.frombuffer(img_binary, dtype=np.uint8)
        #raw image <- jpg
        img = cv2.imdecode(img_jpg, cv2.IMREAD_COLOR)

        results, bad_posture_point, bad_posture_msg_list = main_detect_prevent_hunchback(self.pose, cv2_img_ndarray=img)

        return results, bad_posture_point, bad_posture_msg_list



    #保存する場合
    def save_img(self, capture_img_path, img_base64):
        #binary <- string base64
        img_binary = base64.b64decode(img_base64)
        #jpg <- binary
        img_jpg=np.frombuffer(img_binary, dtype=np.uint8)
        #raw image <- jpg
        img = cv2.imdecode(img_jpg, cv2.IMREAD_COLOR)
        #デコードされた画像の保存先パス
        #画像を保存
        
        results, bad_posture_point, bad_posture_msg_list = main_detect_prevent_hunchback(self.pose, cv2_img_ndarray=img)
        cv2.imwrite(capture_img_path, img)
        return "SUCCESS", results, bad_posture_point, bad_posture_msg_list