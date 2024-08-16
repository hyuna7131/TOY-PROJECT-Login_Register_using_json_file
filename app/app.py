from flask import Flask, request, redirect, url_for, render_template, session
###import hashlib
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 세션 암호화에 사용되는 비밀 키

'''def hash_password(password):
    """비밀번호를 해시화하여 안전하게 저장"""
    return hashlib.sha256(password.encode()).hexdigest()'''

def read_users():
    """파일에서 사용자 정보를 읽어옴"""
    if not os.path.exists("users.txt"):
        return {}
    users = {}
    with open("users.txt", "r") as file:
        for line in file:
            username, password = line.strip().split(':')
            users[username] = password
    return users

def write_user(username, password):
    """JSON 파일에 사용자 정보를 저장"""
    users = read_users()
    users[username] = password
    with open("users.json", "w") as file:
        json.dump(users, file)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ###hashed_password = hash_password(password)
        
        users = read_users()
        if username in users:
            return "이미 존재하는 사용자입니다. <a href='/register'>다시 시도</a>"
        
        write_user(username, password)###hashed_password)
        return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ###hashed_password = hash_password(password)
        
        users = read_users()
        if username in users and users[username] == password:###hashed_password:
            session['username'] = username
            return redirect(url_for('home'))
        
        return "사용자 이름이나 비밀번호가 잘못되었습니다. <a href='/login'>다시 시도</a>"
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="8000", debug=True)
