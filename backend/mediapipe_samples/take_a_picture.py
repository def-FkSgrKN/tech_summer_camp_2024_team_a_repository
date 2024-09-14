import cv2
import time
import os

#カメラの設定　デバイスIDは0
cap = cv2.VideoCapture(0)
picture_num = 0
picture_folder_name = "picture_folder"
picture_file_name_head = "joint_test"
picture_file_name_tail = ".png"

take_pictures_start_time = time.time()
take_pictures_end_time = take_pictures_start_time
take_pictures_delta_time = 5 #[s]

#繰り返しのためのwhile文
while True:
    #カメラからの画像取得
    ret, frame = cap.read()

    #カメラの画像の出力
    cv2.imshow('camera' , frame)

    take_pictures_end_time = time.time()

    #写真撮影時間的な条件
    if take_pictures_end_time - take_pictures_start_time > take_pictures_delta_time:
        picture_file_name = picture_file_name_head + str(picture_num) + picture_file_name_tail
        
        picture_folder_path = os.path.join(picture_folder_name, picture_file_name)
        
        cv2.imwrite(picture_folder_path,frame)

        picture_num += 1
        take_pictures_start_time = time.time()

    #繰り返し分から抜けるためのif文
    key =cv2.waitKey(10)
    if key == 27:
        break

#メモリを解放して終了するためのコマンド
cap.release()
cv2.destroyAllWindows()