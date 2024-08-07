#https://www.youtube.com/watch?reload=9&v=VtJ-fGm4gNg

from flask import Flask
from flask import render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)

##データベース作成
#blog.dbという名前のDBを作成（授業で/temp/test.db → blog.dbに）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'


db = SQLAlchemy(app)

#classを用いてDBを定義（授業でUser → Postに）
class Post(db.Model):
    #ブログＩＤ．IDはint型，primary_keyはメインのキー
    id = db.Column(db.Integer, primary_key = True)
    #ブログタイトル．titleはStr型（授業でusername → titleに），50文字以内，uniqueは同じものを認めない，nullableは空白を認める
    title = db.Column(db.String(50), unique = True, nullable = False)
    #ブログ本文．上と同様（授業でemail → bodyに）
    body = db.Column(db.String(300), unique = True, nullable = False)
    #ブログ日時．現在時刻を自動で入力
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.now(pytz.timezone('Asia/Tokyo')))


@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        #登録したすべてのデーターを取ってくる
        posts = Post.query.all()
        #得たpostsをindex.htmlに渡す
        return render_template('index.html', Posts = posts)


#新規追加処理，（GETとPOSTも受け付ける）
@app.route('/create', methods = ['GET','POST'])
def create():
    if request.method == 'POST':
        #新規作成formのtitleをTitleに代入する（bodyも同様）
        Title = request.form.get('title')
        Body = request.form.get('body')
        #Titleを19行目のPostのtitleに代入する（Bodyも同様）
        post = Post(title = Title, body = Body)
        
        #POSTにpostを追加
        db.session.add(post)
        #POSTを変更して保存する
        db.session.commit()
        #初期画面（ここでは「'/'」）に戻る
        return redirect('/')
    else:
        return render_template('create.html')
  
#編集処理  
@app.route('/<int:id>/update', methods = ['GET','POST'])
def update(id):
    #58行目のidをもとにPostのデータを取得
    post = Post.query.get(id)
    
    #「編集」ボタンが押されたとき
    if request.method == 'GET':
        return render_template('update.html', post = post)
    
    #「更新」ボタンが押されたとき
    if request.method == 'POST':
        #更新formのtitleをpost.titleに代入する（bodyも同様）
        post.title = request.form.get('title')
        post.body = request.form.get('body')
        
        #postを変更して保存する
        db.session.commit()
        #初期画面（ここでは「'/'」）に戻る
        return redirect('/')
    
#削除処理
@app.route('/<int:id>/delete', methods = ['GET','POST'])
def delete(id):
    #58行目のidをもとにPostのデータを取得
    post = Post.query.get(id)
    
    #「削除」ボタンが押されたとき
    if request.method == 'GET':
        return render_template('delete.html', post = post)
    
    #「完全に削除」ボタンが押されたとき
    if request.method == 'POST':
        #dbのpostを削除する
        db.session.delete(post)        
        #postを変更して保存する
        db.session.commit()
        #初期画面（ここでは「'/'」）に戻る
        return redirect('/')

    

###POST,GETの違い###
#POST...新規作成時，送信するときに使う
#GET...Webページにアクセス時使われる

###「blog.db」を作成###（←？？？）
#「python」で対話モードに
#「from app import db」
#「db.create_all()」
###結果###
#「blog.db」が左にできる