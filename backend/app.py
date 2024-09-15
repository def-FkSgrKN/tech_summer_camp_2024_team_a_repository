import uuid
import os
import time

from flask import Flask, session, request, jsonify, render_template, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

from service import img_process_service


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hunchback_users.db' #UserDB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = 'your_secret_key'

#セッションの寿命
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1) #セッションの寿命1分
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30) #セッションの寿命30日

db = SQLAlchemy(app)

"""
mediapipe関連をグローバル変数で管理
グローバル変数が良くない場合 キャッシュ
"""
img_process_service_instance = img_process_service()

# Userモデルの定義
class UserRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    data = db.Column(db.String(120), nullable=False)

print(UserRecord.__tablename__) #実際の表の名前:user_record


# UserIDのみの表 親表
class User_ID_Table(db.Model):
    user_id = db.Column(db.String(36), primary_key=True)

print(User_ID_Table.__tablename__) #実際の表の名前:user_id__table



# UserIDに結びついた開始時刻と終了時刻の全userの一覧データ
class User_Posture_Time_Record_Table(db.Model):
    user_id = db.Column(db.String(36), db.ForeignKey('user_id__table.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    posture_detect_start_time = db.Column(db.Float, nullable=False)
    posture_detect_end_time = db.Column(db.Float, nullable=False)

print(User_Posture_Time_Record_Table.__tablename__) #実際の表の名前:user__posture__time__record__table
    # 外部参照キー設定
    # 親テーブルのデータが削除されたり更新されたときのカスケード動作を指定
    #user_id = db.Column(db.String(36), db.ForeignKey('UserID_Table.user_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)


"""
姿勢を維持している時間を維持するグローバル変数
"""
#active_user_id_list = ["A", "B"] #現在 このwebアプリを使用しているUserIDのリスト

"""
要変更 GithubAuthを得て得られたUserIDに置き換えるべき場所 
デバッグのため, 現在はこのIDを使用する
"""
global_user_id = "User_ID_Sample"
INIT_HUNCHBACK_JUDGEMENT_ALLOWABLE_NUM = 3 #猫背は初期時に3回の残基が与えられる

hunchback_judgement_allowable_num = {} #Userに紐づいた残りの猫背許容回数の辞書
posture_detect_start_time_global_dict = {} #Userに紐づいた開始時刻の辞書
posture_detect_end_time_global_dict = {} #Userに紐づいた終了時刻の辞書

# データベースを作成
with app.app_context():
    db.create_all()

# ユーザーを識別するためにUUIDをセッションに保存
@app.before_request
def ensure_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # 一意のUUIDを生成してセッションに保存

# ユーザーの記録を保存するエンドポイント
@app.route('/save', methods=['POST'])
def save_record():
    user_id = session['user_id']  # セッションからユーザーIDを取得
    data = request.json.get('data')  # リクエストからデータを取得

    if data:
        # ユーザーの記録をデータベースに保存
        new_record = UserRecord(user_id=user_id, data=data)
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"message": "Record saved"}), 201
    return jsonify({"error": "No data provided"}), 400

# ユーザーの記録を取得するエンドポイント
@app.route('/records', methods=['GET'])
def get_records():
    user_id = session['user_id']  # セッションからユーザーIDを取得
    records = UserRecord.query.filter_by(user_id=user_id).all()
    
    return jsonify([{"id": record.id, "data": record.data} for record in records]), 200

# メインページのルート(1頁目)
@app.route('/')
def index():
    return render_template('index.html')


# 姿勢矯正ページ (2頁目)
"""
姿勢矯正キャプチャ開始フラグはこの中で呼び出される
"""
"""
#フロントエンドと合体させるとき
@app.route('/posture_correction<string:user_id>')
def posture_correction(user_id):
"""
#デバッグ時
@app.route('/posture_correction')
def posture_correction():

    """
    data = request.get_json()
    user_id = data.get('user_id') #フロントエンドと合体させるとき
    """
    user_id = global_user_id #デバッグ時

    #そのユーザのキャプチャ開始時刻(猫背になった時刻ではない)
    posture_detect_start_time_global_dict[user_id] = time.time()
    hunchback_judgement_allowable_num[user_id] = INIT_HUNCHBACK_JUDGEMENT_ALLOWABLE_NUM
    
    print("posture_detect_start_time_global_dict[user_id]=" + str(posture_detect_start_time_global_dict[user_id]))

    return render_template('posture_correction.html')

"""
ユーザの表への操作
"""
# 特定のユーザの過去の全データを問合わせる
"""
#フロントエンドと合体させるとき
@app.route('/search_past_all_user_data<string:user_id>', methods=['GET'])
def search_past_all_user_data(user_id):
"""
#デバッグ時
@app.route('/search_past_all_user_data', methods=['GET'])
def search_past_all_user_data():
    # user_idに基づいてユーザーデータを取得
    
    """
    data = request.get_json()
    user_id = data.get('user_id') #フロントエンドと合体させるとき
    """
    user_id = global_user_id #デバッグ時

    past_all_user_data = User_Posture_Time_Record_Table.query.filter_by(id=user_id).all()
    
    if past_all_user_data:
        # データが見つかった場合
        return jsonify({
            'posture_detect_start_time': past_all_user_data.posture_detect_start_time,
            'posture_detect_end_time': past_all_user_data.posture_detect_end_time
        })
    else:
        # データが見つからない場合
        return 'User not found', 404

"""
バックエンド側で, 
Userが終了フラグを検知した後に呼び出される
"""
# 特定のユーザの過去の全データへ記録する
def save_now_user_data(user_id):

    #if data:
    # ユーザーの記録をデータベースに保存
    new_record = User_Posture_Time_Record_Table(user_id=user_id, 
                                                posture_detect_start_time=posture_detect_start_time_global_dict[user_id], 
                                                posture_detect_end_time=posture_detect_end_time_global_dict[user_id]
                                                )
    db.session.add(new_record)
    db.session.commit()
      

"""
Qiita, [python] Webカメラからキャプチャした画像をサーバに送信して保存する, 
https://qiita.com/h_000/items/e5ff1152aae8c67af476
"""
"""
姿勢矯正キャプチャ終了フラグはこの中で呼び出される
"""
"""
#フロントエンドとの合体
@app.route('/capture_img<string:user_id>', methods=['POST'])
def capture_img(user_id):
"""
#デバッグ
@app.route('/capture_img', methods=['POST'])
def capture_img():
    print("capture_imgが実行されました")

    """
    リクエストボディからjsonで受け取る方式へ仕様変更
    data = request.get_json()
    base64_img = data.get("img")
    """
    
    data = request.get_json()
    #print("data=")
    #print(data)
    #print("\n")

    base64_img = data.get("img")
    #print("base64_img=")
    #print(base64_img)
    #print("\n")

    user_id = global_user_id


    results, bad_posture_point, bad_posture_msg_list = img_process_service_instance.detect_hunchback_from_img(base64_img)

    """
    悪い姿勢ポイントが0より大きいと猫背判定として扱われる
    """
    hunchback_judgement = False

    if bad_posture_point > 0:
        hunchback_judgement = True
        hunchback_judgement_allowable_num[user_id] -= 1 #猫背の回数だけ減少する


    print("results=" + str(results))
    print("bad_posture_point=" + str(bad_posture_point))
    print("bad_posture_msg_list=" + str(bad_posture_msg_list))
    print("\n")


    """
    姿勢推定キャプチャ終了フラグ
    残基が0になったら終了
    """
    if hunchback_judgement_allowable_num[user_id] == 0:
        posture_detect_end_time_global_dict[user_id] = time.time()
        print("posture_detect_end_time_global_dict[user_id]=" + str(posture_detect_end_time_global_dict[user_id]))

        
        print("hunchback_judgement_allowable_num=" + str(hunchback_judgement_allowable_num))
        print("posture_detect_start_time_global_dict=" + str(posture_detect_start_time_global_dict))
        print("posture_detect_end_time_global_dict=" + str(posture_detect_end_time_global_dict))

        """
        リターン後, 開始時のページに飛べた方が良い
        """

        # JSONデータに基づいて処理を行う
        response_data = {
            "end_flag":True, 
            "hunchback_judgement_allowable_num":hunchback_judgement_allowable_num[user_id], #残基
            "posture_detect_start_time_global_dict": posture_detect_start_time_global_dict[user_id],
            "posture_detect_end_time_global_dict": posture_detect_end_time_global_dict[user_id],
            "hunchback_judgement": hunchback_judgement,
            "hunchback_message":bad_posture_msg_list
        }



    else:
   
        # JSONデータに基づいて処理を行う
        response_data = {
            "end_flag":False, #終了フラグ
            "hunchback_judgement_allowable_num":hunchback_judgement_allowable_num[user_id], #残基
            "posture_detect_start_time_global_dict": 0, #開始時刻
            "posture_detect_end_time_global_dict": 0, #終了時刻
            "hunchback_judgement": hunchback_judgement, #猫背判定
            "hunchback_message":bad_posture_msg_list #猫背の説明
        }
        print("response_data=")
        print(response_data)

        
        return jsonify(response_data)


"""
フロントエンドで結果表示後
フロントエンド --> バックエンド
へ閉じる指示が送られてから, 終了

終了フラグ後に実際に, 動作を停止し, 元のリンクに戻る
"""
@app.route('/capture_img_end')
def capture_img_end():

    user_id = global_user_id

    """
    終了フラグのときにDBに保存
    """
    save_now_user_data(user_id)

    """
    終了し, DBに追加し終えたUserの開始終了時刻, 猫背残基の辞書からキーを削除
    """
    hunchback_judgement_allowable_num.pop(user_id)
    posture_detect_start_time_global_dict.pop(user_id)
    posture_detect_end_time_global_dict.pop(user_id)

    return redirect("/") 


"""
DB確認用
"""
# DBの内容を表示するルート
@app.route('/view_hunchback_users_db')
def view_users():
    # 全てのユーザーを取得
    users = User_Posture_Time_Record_Table.query.all()

    # 取得したユーザーをテンプレートで表示
    return render_template('view_users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)