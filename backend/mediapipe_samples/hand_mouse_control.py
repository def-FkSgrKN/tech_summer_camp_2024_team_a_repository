import cv2
import pyautogui
import mediapipe as mp
import time
import numpy as np
#import SendToRaspPi as rp#SendToRaspi.py ファイルを同フォルダに保存する
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
# For static images:
decide = True
count = 0
ptime = 0
close_check = False
open_check = False

"""
Qiita, MediaPipeを使ってRCカーのコントロール（ジェスチャーインターフェース）,
https://qiita.com/sthasmn/items/d430880f5c0fe19f83c7
"""

def open_check_by_distance(keypoints, center):
    def thumb_open_check(keypoints, center):
        d4 = np.sqrt(np.square(keypoints[4][0] - center[0]) + np.square(keypoints[4][1] - center[1]))
        d3 = np.sqrt(np.square(keypoints[3][0] - center[0]) + np.square(keypoints[3][1] - center[1]))
        if d4 > d3:
            return True
        else:
            return False
    def index_open_check(keypoints, center):
        d5 = np.sqrt(np.square(keypoints[5][0] - center[0]) + np.square(keypoints[5][1] - center[1]))
        d6 = np.sqrt(np.square(keypoints[6][0] - center[0]) + np.square(keypoints[6][1] - center[1]))
        d7 = np.sqrt(np.square(keypoints[7][0] - center[0]) + np.square(keypoints[7][1] - center[1]))
        d8 = np.sqrt(np.square(keypoints[8][0] - center[0]) + np.square(keypoints[8][1] - center[1]))
        if d8 > d7 > d6 > d5:
            return True
        else:
            return False
    def middle_open_check(keypoints, center):
        d9 = np.sqrt(np.square(keypoints[9][0] - center[0]) + np.square(keypoints[9][1] - center[1]))
        d10 = np.sqrt(np.square(keypoints[10][0] - center[0]) + np.square(keypoints[10][1] - center[1]))
        d11 = np.sqrt(np.square(keypoints[11][0] - center[0]) + np.square(keypoints[11][1] - center[1]))
        d12 = np.sqrt(np.square(keypoints[12][0] - center[0]) + np.square(keypoints[12][1] - center[1]))
        if d12 > d11 > d10 > d9:
            return True
        else:
            return False
    def ring_open_check(keypoints, center):
        d13 = np.sqrt(np.square(keypoints[13][0] - center[0]) + np.square(keypoints[13][1] - center[1]))
        d14 = np.sqrt(np.square(keypoints[14][0] - center[0]) + np.square(keypoints[14][1] - center[1]))
        d15 = np.sqrt(np.square(keypoints[15][0] - center[0]) + np.square(keypoints[15][1] - center[1]))
        d16 = np.sqrt(np.square(keypoints[16][0] - center[0]) + np.square(keypoints[16][1] - center[1]))
        if d16 > d15 > d14 > d13:
            return True
        else:
            return False
    def pinky_open_check(keypoints, center):
        d17 = np.sqrt(np.square(keypoints[17][0] - center[0]) + np.square(keypoints[17][1] - center[1]))
        d18 = np.sqrt(np.square(keypoints[18][0] - center[0]) + np.square(keypoints[18][1] - center[1]))
        d19 = np.sqrt(np.square(keypoints[19][0] - center[0]) + np.square(keypoints[19][1] - center[1]))
        d20 = np.sqrt(np.square(keypoints[20][0] - center[0]) + np.square(keypoints[20][1] - center[1]))
        if d20 > d19 > d18 > d17:
            return True
        else:
            return False
    thumb = thumb_open_check(keypoints, center)
    index = index_open_check(keypoints, center)
    middle = middle_open_check(keypoints, center)
    ring = ring_open_check(keypoints, center)
    pinky = pinky_open_check(keypoints, center)
    if thumb == True and index == True and middle == True and ring == True and pinky == True:
        return True
    else:
        return False

def close_check_by_distance(keypoints, center): #tested OK
   d3 = np.sqrt(np.square(keypoints[3][0] - center[0]) + np.square(keypoints[3][1] - center[1]))
   d4 = np.sqrt(np.square(keypoints[4][0] - center[0]) + np.square(keypoints[4][1] - center[1]))
   d5 = np.sqrt(np.square(keypoints[5][0] - keypoints[0][0]) + np.square(keypoints[5][1] - keypoints[0][1]))
   d8 = np.sqrt(np.square(keypoints[8][0] - keypoints[0][0]) + np.square(keypoints[8][1] - keypoints[0][1]))
   d9 = np.sqrt(np.square(keypoints[9][0] - keypoints[0][0]) + np.square(keypoints[9][1] - keypoints[0][1]))
   d12 = np.sqrt(np.square(keypoints[12][0] - keypoints[0][0]) + np.square(keypoints[12][1] - keypoints[0][1]))
   d13 = np.sqrt(np.square(keypoints[13][0] - keypoints[0][0]) + np.square(keypoints[13][1] - keypoints[0][1]))
   d16 = np.sqrt(np.square(keypoints[16][0] - keypoints[0][0]) + np.square(keypoints[16][1] - keypoints[0][1]))
   d17 = np.sqrt(np.square(keypoints[17][0] - keypoints[0][0]) + np.square(keypoints[17][1] - keypoints[0][1]))
   d20 = np.sqrt(np.square(keypoints[20][0] - keypoints[0][0]) + np.square(keypoints[20][1] - keypoints[0][1]))

   if d8 < d5 and d12 < d9 and d16 < d13 and d20 < d17 and d4 < d3:
       return True
   else:
       return False

def take_coordinates(coordinates):
  if coordinates == None:
    return 0
  keypoints = []
  for data_point in coordinates:
    xyz_datapoints = data_point.landmark
    for xyz in xyz_datapoints:
      X_value = round(xyz.x*10000, 2)
      Y_value = round(xyz.y*10000, 2)
      Z_value = round(xyz.z, 3)
      xy = [X_value,Y_value, Z_value]
      keypoints.append(xy)
  return keypoints

def centroid_palm(keypoints): #calculation not correct. Do it again
    if keypoints == 0:
        return 0
    x_bar = (keypoints[0][0] + keypoints[9][0])/2
    x_bar = round(x_bar, 2)
    y_bar = (keypoints[0][1] + keypoints[9][1])/2
    y_bar = round(y_bar, 2)
    return x_bar, y_bar

def get_angle(keypoints, center):
    #(x',y')=(x, max-y)
    if keypoints == 0:
        return 0

    center = list(center)
    wrist = list(keypoints)
    wrist[1] = 10000-wrist[1] # y' = max - y
    center[1] = 10000-center[1] # y' = max - y
    Y = center[1]-wrist[1]
    X = center[0]-wrist[0]
    try:
        m = Y/X
    except ZeroDivisionError:
        m = 0
    angle = np.arctan(m)*180/(np.pi)
    if X > 0 and Y < 0:
        angle = angle + 360
    elif X < 0 and Y > 0:
        angle = angle + 180
    elif X < 0 and Y < 0:
        angle = angle + 180
    return round(angle, 1)

def motor(value):#モーター制御のために必要な値にmappingを行う。モーターによって値が変わる
    leftMin = -0.3
    leftMax = 0.1
    rightMin = 6.5
    rightMax = 5.5

    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def calculate(keypoints):
    global decide
    global close_check
    global open_check

    open_or_close = "no_key_point"
    angle = 0 

    if keypoints == 0:
        #rp.send(f"{0}, {90}")
        return open_or_close, angle

    # ひらの中心を求める
    center = centroid_palm(keypoints)
    #手の傾きの検出
    angle = get_angle(keypoints[0], center)
    # マウスを制御するためのPWM値を検出
    motor_value = round(motor(keypoints[12][2]), 1)
    #手がopenであることの確認
    open_check = open_check_by_distance(keypoints, center)
    #openならば、RCカーがエンジンON（仮定）



    if open_check == True:
        open_or_close = "open"
        # PCからRaspberry Piへモーターとサーボーの制御をするために送信を行う。
        #rp.send(f"{motor_value}, {int(angle)}")
        print(f"sending{motor_value}, {angle}")
        #print("手が開いている")
    # closeならば、RCカーがエンジンOFF（仮定）
    elif close_check:
        #print("手が閉じている")
        open_or_close = "close"
        #rp.send(f"{6.0}, {90}")
    return open_or_close, angle



# For webcam input:

# Webカメラから入力
cap = cv2.VideoCapture(0)

pTime = 0
with mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5) as hands:

  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
    #FPSの計算の為
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime


    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    cv2.putText(image, f'FPS: {int(fps)}', (800, 720), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)
    keypoints = take_coordinates(results.multi_hand_landmarks)
    if keypoints != 0:
        place = (int((keypoints[12][0]) / 10), int((keypoints[12][1]) / 15))
        cv2.putText(image, f'{float(get_angle(keypoints[0], centroid_palm(keypoints)))}', place, cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 3)
    if keypoints == 0:
        place = (200, 200)

    # この関数が全ての数値を計算してる
    open_or_close, angle = calculate(keypoints)

    if open_or_close == "open":
        print("解放")
        
        RIGHT_HAND_ANGLE_MIN = 30
        RIGHT_HAND_ANGLE_MAX = 210
        
        ANGLE_RANGE = RIGHT_HAND_ANGLE_MAX - RIGHT_HAND_ANGLE_MIN
        Separate_num = 8

        DELTA_PART_ANGLE = ANGLE_RANGE/Separate_num
        mouse_move_vector = np.zeros(2)

        for i in range(Separate_num):
            if RIGHT_HAND_ANGLE_MIN + DELTA_PART_ANGLE*i <= angle < RIGHT_HAND_ANGLE_MIN + DELTA_PART_ANGLE*(i+1):
                mouse_move_vec_angle = i*360/Separate_num
                mouse_move_vector[0] = 30*np.cos(np.radians(mouse_move_vec_angle))
                mouse_move_vector[1] = -30*np.sin(np.radians(mouse_move_vec_angle))
                print("mouse_move_vec_angle=" + str(mouse_move_vec_angle) + ", mouse_move_vector=" + str(mouse_move_vector))
                
                now_mouse_pos = pyautogui.position()
                pyautogui.moveTo(now_mouse_pos[0] + mouse_move_vector[0], now_mouse_pos[1] + mouse_move_vector[1])

        """
        #315 ~ 360 or 0~45
        if 315 < angle <= 360 or 0 < angle <= 45:
            print("angle=" + str(angle) + ", 右向き(x正)")

        #45 ~ 135
        elif 45 < angle <= 135:
            print("angle=" + str(angle) + ", 上向き(y正)")

        #135 ~ 225
        elif 135 < angle <= 225:
            print("angle=" + str(angle) + ", 左向き(y正)")

        #225 ~ 315
        elif 225 < angle < 315:
            print("angle=" + str(angle) + ", 下向き(y正)")
        """

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()