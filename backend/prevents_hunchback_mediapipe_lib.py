
import cv2
import os
import numpy as np
import mediapipe as mp
import math
import time
import datetime

"""
Qiita, pythonとmediapipeを用いた座った姿勢における肩と腰の角度の検出, 
https://qiita.com/futurecreatenow/items/9c9a76383b1ccdf1a8fc
"""


#体の部位の座標（x,y,z）と部位の可視性（v）を取得
def get_coordinate(results, landmark_num):
    parts_array = {"x":0, "y":0, "z":0,"v":0}
    parts_array["x"] = results.pose_landmarks.landmark[landmark_num].x
    parts_array["y"] = results.pose_landmarks.landmark[landmark_num].y
    parts_array["z"] = results.pose_landmarks.landmark[landmark_num].z
    parts_array["v"] = results.pose_landmarks.landmark[landmark_num].visibility
    return parts_array



##main##
#ファイルの存在チェック
#print(os.path.exists('picture/sample.jpg'))



#ファイルの読み込み
#image = cv2.imread('picture/sample.jpg')


def main_detect_prevent_hunchback(pose, cv2_img_ndarray):


    #results = holistic.process(cv2.cvtColor(cv2_img_ndarray, cv2.COLOR_BGR2RGB))
    results = pose.process(cv2.cvtColor(cv2_img_ndarray, cv2.COLOR_BGR2RGB))

    #左右の歪み:各1ポイント, #猫背:各3ポイント
    RIGHT_LEFT_BAD_POINT = 1
    HUNCHBACK_BAD_POINT = 3
    bad_posture_point = 0
    bad_posture_msg_list = []

    try:

        #左右肩の座標の取得
        L_shoulder = get_coordinate(results, 11)
        R_shoulder = get_coordinate(results, 12)

        #左右耳の座標の取得
        L_ear = get_coordinate(results, 8)
        R_ear = get_coordinate(results, 7)

        #左右首の座標の取得
        L_neck = get_coordinate(results, 10)
        R_neck = get_coordinate(results, 9)

        #腰と肩の角度の計算
        print("""R_shoulder["v"]=""" + str(R_shoulder["v"]))
        print("""L_shoulder["v"]=""" + str(L_shoulder["v"]))
        print("\n")

        #左右のx, y, zの差を出力
        if (L_shoulder["v"] > 0.60 and R_shoulder["v"] > 0.60):
            #delta_sholder_x = L_shoulder["x"] - R_shoulder["x"]
            delta_sholder_y = L_shoulder["y"] - R_shoulder["y"]
            delta_sholder_z = L_shoulder["z"] - R_shoulder["z"]

            if delta_sholder_z > 0.25:
                bad_posture_msg_list.append("右肩の方が手前に来て姿勢が歪んでいます")
                bad_posture_point += RIGHT_LEFT_BAD_POINT

            elif delta_sholder_z < -0.25:
                bad_posture_msg_list.append("左肩の方が手前に来て姿勢が歪んでいます")
                bad_posture_point += RIGHT_LEFT_BAD_POINT


            if delta_sholder_y > 0.1:
                bad_posture_msg_list.append("左肩の方が上に来て姿勢が歪んでいます")
                bad_posture_point += RIGHT_LEFT_BAD_POINT

            elif delta_sholder_y < -0.1:
                bad_posture_msg_list.append("右肩の方が上に来て姿勢が歪んでいます")
                bad_posture_point += RIGHT_LEFT_BAD_POINT


            """
            どれだけ首が前に出ているかを見る
            """
            #どれだけ首が前に出ているかを見る
            ave_sholder_z = (L_shoulder["z"] + R_shoulder["z"])/2
            
            
            #左右のx, y, zの差を出力
            if (L_ear["v"] > 0.60 and R_ear["v"] > 0.60):
                ave_ear_z = (L_ear["z"] + R_ear["z"])/2
                delta_ave_shoulder_ear_z = ave_sholder_z - ave_ear_z
                #print("delta_ave_shoulder_ear_z=" + str(delta_ave_shoulder_ear_z))
                #猫背でないとき delta_ave_shoulder_ear_z=0.08167809247970581
                #猫背のとき delta_ave_shoulder_ear_z=0.2629910111427307
                
                if delta_ave_shoulder_ear_z > 0.25:
                    bad_posture_msg_list.append("首が前に出て, 猫背になっています")
                    bad_posture_point += HUNCHBACK_BAD_POINT

            #左右のx, y, zの差を出力
            elif (L_neck["v"] > 0.60 and R_neck["v"] > 0.60):
                ave_neck_z = (L_neck["z"] + R_neck["z"])/2
                delta_ave_shoulder_neck_z = ave_sholder_z - ave_neck_z
                #print("delta_ave_shoulder_neck_z=" + str(delta_ave_shoulder_neck_z))
                #猫背でないとき delta_ave_shoulder_neck_z=0.3552832007408142
                #猫背のとき delta_ave_shoulder_neck_z=0.627670556306839

                if delta_ave_shoulder_neck_z > 0.6:
                    bad_posture_msg_list.append("首が前に出て猫背になっています")
                    bad_posture_point += HUNCHBACK_BAD_POINT


            #print("delta_sholder_x=" + str(delta_sholder_x))
            #print("delta_sholder_y=" + str(delta_sholder_y))
            #print("delta_sholder_z=" + str(delta_sholder_z))


    except:
        result = None
        
    return results, bad_posture_point, bad_posture_msg_list


def set_video_capture_in_python():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    return mp_pose, pose
    

def main_video_capture_in_python():

    """
    holisticは全身(骨格, 顔, 手) 重い
    """
    #mp_holistic = mp.solutions.holistic
    #holistic = mp_holistic.Holistic(static_image_mode=True,min_detection_confidence=0.5)
    """
    poseは骨格のみ 軽い
    """
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    MAX_BAD_POINT_TH = 1 #ゲームオーバーにならない最大ポイント

    cap = cv2.VideoCapture(0)

    start_time_utc = time.time()
    end_time_utc = start_time_utc

    start_datetime = datetime.datetime.now()
    end_datatime = start_datetime

    #繰り返しのためのwhile文
    while True:
        #カメラからの画像取得
        ret, frame = cap.read()
        
        results, bad_posture_point, bad_posture_msg_list = main_detect_prevent_hunchback(pose, cv2_img_ndarray=frame)
        print("results=" + str(results))
        print("bad_posture_point=" + str(bad_posture_point))
        print("bad_posture_msg_list=" + str(bad_posture_msg_list))

        if MAX_BAD_POINT_TH < bad_posture_point:
            print("ゲームオーバー")
            end_time_utc = time.time()
            end_datatime = datetime.datetime.now()
            break
        
        try:
            # ポーズを描画
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        except:
            print("resultがNone")

        #カメラの画像の出力
        cv2.imshow('camera' , frame)

        #繰り返し分から抜けるためのif文
        if cv2.waitKey(5) & 0xFF == 27:
            break

    #メモリを解放して終了するためのコマンド
    cap.release()
    cv2.destroyAllWindows()

    print("~結果発表~")
    print("開始時刻:" + str(start_datetime) + ", 終了時刻:" + str(end_datatime))
    print("持続時間" + str(end_time_utc - start_time_utc))

if __name__ == "__main__":
    main_video_capture_in_python()



