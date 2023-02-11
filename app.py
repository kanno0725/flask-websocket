# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import time
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# cors_allowed_originは本来適切に設定するべき
socketio = SocketIO(app, cors_allowed_origins='*')

# ユーザー数
user_count = 0
# 現在のテキスト
text = ""

is_stop = False

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('/pipe')
def pipe():
    print('test')
    return 'test'

# ユーザーが新しく接続すると実行
@socketio.on('connect')
def connect(auth):
    print('hello')
    global user_count, text
    user_count += 1
    # 接続者数の更新（全員向け）
    emit('count_update', {'user_count': user_count}, broadcast=True)
    # テキストエリアの更新
    emit('text_update', {'text': text})


# ユーザーの接続が切断すると実行
@socketio.on('disconnect')
def disconnect():
    global user_count
    user_count -= 1
    # 接続者数の更新（全員向け）
    emit('count_update', {'user_count': user_count}, broadcast=True)


# テキストエリアが変更されたときに実行
@socketio.on('text_update_request')
def text_update_request(json):
    print('change')
    global text
    text = json["text"]
    # 変更をリクエストした人以外に向けて送信する
    # 全員向けに送信すると入力の途中でテキストエリアが変更されて日本語入力がうまくできない
    emit('text_update', {'text': text}, broadcast=True, include_self=False)

@socketio.on('start')
def button():
    print('pushed start-button')
    global is_stop
    is_stop = False
    # emit('button',{'button_state':'ON'}, broadcast=True)
    #for i in range(10):
    emit('start_button_state_update', broadcast=True)
    while(not is_stop):
        emit('graph_update',{'data': random.random()}, broadcast=True)
        time.sleep(1)

@socketio.on('end')
def button():
    print('pushed end-button')
    global is_stop
    is_stop = True
    # emit('button',{'button_state':'ON'}, broadcast=True)
    emit('end_button_state_update', broadcast=True)

if __name__ == '__main__':
    # 本番環境ではeventletやgeventを使うらしいが簡単のためデフォルトの開発用サーバーを使う
    socketio.run(app, debug=True)