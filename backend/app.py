import json
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
    #user_idとposture_detect_start_timeとの復号主キーとする
    user_id = db.Column(db.String(36), db.ForeignKey('user_id__table.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    posture_detect_start_time = db.Column(db.Float, primary_key=True)
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

"""
クライアントごとにsessionが存在する
ため, そのUserのsessionが初期化される
"""
def initialize_session(user_id):
    # セッションの初期化
    session['hunchback_judgement_allowable_num'] = 3  # 許容回数を初期化
    session['posture_detect_start_time'] = 0       # 開始時刻を初期化
    session['posture_detect_end_time'] = 0         # 終了時刻を初期化
    session['user_id'] = user_id          # user_idで誰のsessionかを判断するために重要 ユーザーIDをサンプルで初期化


"""
hunchback_judgement_allowable_num = {} #Userに紐づいた残りの猫背許容回数の辞書
posture_detect_start_time_global_dict = {} #Userに紐づいた開始時刻の辞書
posture_detect_end_time_global_dict = {} #Userに紐づいた終了時刻の辞書
"""



# データベースを作成
with app.app_context():
    db.create_all()

# ユーザーを識別するためにUUIDをセッションに保存
"""
サンプル例

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

"""

"""
セッションの初期化
"""
# メインページのルート(1頁目)
@app.route('/')
def index():
    page_name = "index"

    
    #そのユーザのセッションを初期化
    user_id_from_token = global_user_id
    initialize_session(user_id_from_token)

    #return render_template('index.html')
    return jsonify({"page_name":page_name})


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
    session check
    """
    user_id_from_token = global_user_id

    """
    開始フラグとして, 開始時刻を0でない現在時刻にする
    """
    user_id_from_token = global_user_id
    user_id_from_session = session.get("user_id")
   
    #一致していない場合 おかしいのでerror
    if user_id_from_token != user_id_from_session:
        session.clear()  # セッションをクリアする
        return jsonify({"status_message": "Unauthorized access, please log in again"}), 403

    session['posture_detect_start_time'] = time.time()

    page_name = "posture_correction"
    return jsonify({"page_name":page_name}), 200
    #return render_template('posture_correction.html')


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
    
    user_id_from_token = global_user_id
    user_id_from_session = session.get("user_id")
   
    #一致していない場合 おかしいのでerror
    if user_id_from_token != user_id_from_session:
        session.clear()  # セッションをクリアする
        return jsonify({"status_message": "Unauthorized access, please log in again"}), 403

    

    past_all_specified_user_data_list = User_Posture_Time_Record_Table.query.filter_by(user_id=user_id_from_token).all()
    #print("past_all_user_data=")
    #print(past_all_user_data)

    
    if past_all_specified_user_data_list:
        # データが見つかった場合
        posture_detect_start_time_list =  [past_all_specified_user_data.posture_detect_start_time for past_all_specified_user_data in past_all_specified_user_data_list]
        posture_detect_end_time_list =  [past_all_specified_user_data.posture_detect_end_time for past_all_specified_user_data in past_all_specified_user_data_list]

        return jsonify({
            'posture_detect_start_time_list': posture_detect_start_time_list,
            'posture_detect_end_time_list': posture_detect_end_time_list
        }), 200
    else:
        # データが見つからない場合
        return jsonify({"status_message":"User not found"}), 404

"""
バックエンド側で, 
Userが終了フラグを検知した後に呼び出される
"""
# 特定のユーザの過去の全データへ記録する
def save_now_user_data(user_id):

    #if data:
    # ユーザーの記録をデータベースに保存
    new_record = User_Posture_Time_Record_Table(user_id=user_id, 
                                                posture_detect_start_time=session['posture_detect_start_time'],
                                                posture_detect_end_time=session['posture_detect_end_time']
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

# 静的ファイル（index.htmlなど）を提供するためのルート
#試験用(実装外)
@app.route('/capture_img_front_debug')
def capture_img_front_debug():
    return app.send_static_file('capture_img_front_debug.html')  # staticフォルダからindex.htmlを返す

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

    """
    session check
    """
    user_id_from_token = global_user_id
    user_id_from_session = session.get("user_id")
    #一致していない場合 おかしいのでerror
    if user_id_from_token != user_id_from_session:
        session.clear()  # セッションをクリアする
        return jsonify({"status_message": "Unauthorized access, please log in again"}), 403


    results, bad_posture_point, bad_posture_msg_list = img_process_service_instance.detect_hunchback_from_img(base64_img)

    """
    悪い姿勢ポイントが0より大きいと猫背判定として扱われる
    """
    hunchback_judgement = False

    if bad_posture_point > 0:
        hunchback_judgement = True
        session['hunchback_judgement_allowable_num'] -= 1 #猫背の回数だけ減少する


    print("results=" + str(results))
    print("bad_posture_point=" + str(bad_posture_point))
    print("bad_posture_msg_list=" + str(bad_posture_msg_list))
    print("\n")


    """
    姿勢推定キャプチャ終了フラグ
    残基が0になったら終了
    """
    
    if session['hunchback_judgement_allowable_num'] == 0:
        session['posture_detect_end_time'] = time.time()
        print("session['posture_detect_end_time']=" + str(session['posture_detect_end_time']))

        print("session['hunchback_judgement_allowable_num']=" + str(session['hunchback_judgement_allowable_num']))
        print("session['posture_detect_start_time']=" + str(session['posture_detect_start_time']))
        print("session['posture_detect_end_time']=" + str(session['posture_detect_end_time']))

        """
        リターン後, 開始時のページに飛べた方が良い
        """

        """
        終了フラグのときにDBに保存
        """
        save_now_user_data(user_id_from_token)

        

        # JSONデータに基づいて処理を行う
        response_data = {
            "end_flag":True, 
            "hunchback_judgement_allowable_num":session['hunchback_judgement_allowable_num'], #残基
            "posture_detect_start_time": session['posture_detect_start_time'],
            "posture_detect_end_time": session['posture_detect_end_time'],
            "hunchback_judgement": hunchback_judgement,
            "hunchback_message":bad_posture_msg_list
        }

        """
        猫背計測後の時間が更新されないように -1を与え, ゲーム終了の印とする
        """
        session['hunchback_judgement_allowable_num'] = -1


    elif session['hunchback_judgement_allowable_num'] == -1:
        """
        姿勢耐久が終了かつデータベースに追加されたとき
        """

        response_data = {
            "end_flag":True, 
            "hunchback_judgement_allowable_num":session['hunchback_judgement_allowable_num'], #残基
            "posture_detect_start_time_global_dict": session['posture_detect_start_time'],
            "posture_detect_end_time_global_dict": session['posture_detect_end_time'],
            "hunchback_judgement": hunchback_judgement,
            "hunchback_message":bad_posture_msg_list
        }




    else:
        """
        姿勢耐久が継続しているとき
        """
   
        # JSONデータに基づいて処理を行う
        response_data = {
            "end_flag":False, #終了フラグ
            "hunchback_judgement_allowable_num":session['hunchback_judgement_allowable_num'], #残基
            "posture_detect_start_time_global_dict": session['posture_detect_start_time'], #開始時刻
            "posture_detect_end_time_global_dict": session['posture_detect_end_time'], #終了時刻
            "hunchback_judgement": hunchback_judgement, #猫背判定
            "hunchback_message":bad_posture_msg_list #猫背の説明
        }
        print("response_data=")
        print(response_data)

        
    return jsonify(response_data), 200


"""
フロントエンドで結果表示後
フロントエンド --> バックエンド
へ閉じる指示が送られてから, 終了

終了フラグ後に実際に, 動作を停止し, 元のリンクに戻る
"""
@app.route('/capture_img_end')
def capture_img_end():

    page_name = "capture_img_end"

    """
    終了し, DBに追加し終えたUserの開始終了時刻, 猫背残基の辞書からキーを削除
    """
    #認証されたuser_id
    user_id_from_token = global_user_id

    #sessionのuser_id
    user_id_from_session = session.get("user_id")

    #一致していない場合 おかしいのでerror
    if user_id_from_token != user_id_from_session:
        session.clear()  # セッションをクリアする
        return jsonify({"status_message": "Unauthorized access, please log in again"}), 403

    #一致している場合に削除する
    else:
        session.clear()  # セッションをクリアする
        return jsonify({"page_name":page_name}), 200


    #page_name = "capture_img_end"
    #return jsonify({"page_name":page_name})



"""
DB確認用 実装外
"""
# DBの内容を表示するルート
@app.route('/view_hunchback_users_db')
def view_users():
    """
    session check
    """
    user_id_from_token = global_user_id
    user_id_from_session = session.get("user_id")
    #一致していない場合 おかしいのでerror
    if user_id_from_token != user_id_from_session:
        session.clear()  # セッションをクリアする
        return jsonify({"status_message": "Unauthorized access, please log in again"}), 403

    # 全てのユーザーを取得
    users = User_Posture_Time_Record_Table.query.all()

    # 取得したユーザーをテンプレートで表示
    return render_template('view_users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)