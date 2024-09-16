# tech_summer_camp_2024_team_a_repository
TechSummerCamp2024のteamAのレポジトリです. 

 
"エンジニアの猫背を直します!" は, 
姿勢維持式, 正姿勢持続型啓発ゲームです!
 
# DEMO
 
ここにデモをできれば張る
 

# Features
 
Physics_Sim_Py used [pyxel](https://github.com/kitao/pyxel) only.
 
```python
import pyxel
```
[Pyxel](https://github.com/kitao/pyxel) is a retro game engine for Python.
You can feel free to enjoy making pixel art style physics simulations.
 
# Requirement
 
* Python 3系 
* Flask Flask-SQLAlchemy numpy opencv-python mediapipe pyngrok

* next.js 


# Usage Deploy Installation 
```
Google colablatoryにdeproy_notebookを置いてください

ngrokでアカウントを作ってください

ngrokのアクセスtokenを取得して, googlecolabのシークレットキーにNGROK_SECRET_KEYとして登録してください


notebook中の動かすセル

#ブランチを指定してクローン(バックエンドのみの場合)
!git clone -b develop_fksg_backend_mediapipe https://github.com/def-FkSgrKN/tech_summer_camp_2024_team_a_repository.git

#フロント+バックエンドの場合
!git clone https://github.com/def-FkSgrKN/tech_summer_camp_2024_team_a_repository.git


!pip install Flask Flask-SQLAlchemy numpy opencv-python mediapipe pyngrok

#試しに起動し, port番号を確認 #5000番
!python /content/tech_summer_camp_2024_team_a_repository/backend/app.py


#シークレットキーの設定
from pyngrok import ngrok
from google.colab import userdata

NGROK_AUTH_TOKEN = userdata.get('NGROK_SECRET_KEY')

#あなたのngrokのauth tokenを設定
ngrok.set_auth_token(NGROK_AUTH_TOKEN)


#Githubにもともと入っているDBの削除
!rm /content/tech_summer_camp_2024_team_a_repository/backend/instance/users.db



#Google DriveのDB置き場からDBを取得する
#保存されたDBの読み込み
!cp /content/drive/MyDrive/tech_summer_camp_2024_team_a_backend_deploy_db/instance/hunchback_users.db  /content/tech_summer_camp_2024_team_a_repository/backend/instance/users.db

(URLを確認してください)
# ngrokトンネルを5000番ポートに接続
public_url = ngrok.connect(5000)
print("Public URL:", public_url)


# サーバーの起動（例: Flaskサーバー）
!python /content/tech_summer_camp_2024_team_a_repository/backend/app.py
```

print("Public URL:", public_url)を指定して, 動かしてください

```
#終了後にDBをGoogleDriveへUPする
#上書き強制
!cp -f /content/tech_summer_camp_2024_team_a_repository/backend/instance/users.db  /content/drive/MyDrive/tech_summer_camp_2024_team_a_backend_deploy_db/instance/hunchback_users.db
```


# Note 
左右の肩の歪み, 首を前に出したときに, 猫背として扱う
猫背3回でノックアウト

綺麗な姿勢した時間を計測!
=> 文でどこが悪いのかfeedbackあり

過去の計測時間を確認することができる


# API Reference

バックエンドのAPI仕様



 
# Author
 
* FkSg
* Keisuke
* Fuuma
 
# License
 
"エンジニアの猫背を直します!" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
 
Enjoy making cute physics simulations!
 
Thank you!