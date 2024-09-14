import uuid
import os
from flask import Flask, session, request, jsonify, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

from service import img_process_service


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' #UserDB
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
@app.route('/posture_correction')
def posture_correction():
    return render_template('posture_correction.html')


"""
Qiita, [python] Webカメラからキャプチャした画像をサーバに送信して保存する, 
https://qiita.com/h_000/items/e5ff1152aae8c67af476
"""
@app.route('/capture_img', methods=['POST'])
def capture_img():
    print("capture_imgが実行されました")

    capture_user_img_folder_path = os.path.join("capture_img_root", session['user_id'])
    if not os.path.exists(capture_user_img_folder_path):
        os.mkdir(capture_user_img_folder_path)
    
    capture_user_img_file_path = os.path.join(capture_user_img_folder_path, "img0000.jpg")

    msg, results, bad_posture_point, bad_posture_msg_list = img_process_service_instance.save_img(capture_user_img_file_path, request.form["img"])
    print("results=" + str(results))
    print("bad_posture_point=" + str(bad_posture_point))
    print("bad_posture_msg_list=" + str(bad_posture_msg_list))
    print("\n")
    
    return make_response(msg)

if __name__ == '__main__':
    app.run(debug=True)