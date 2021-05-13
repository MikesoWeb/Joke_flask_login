import os, random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

login_ = 'mike'
password_ = '12345'

all_user_foto = ['static/img/' + i for i in os.listdir('static/img') if i != 'user_foto.jpg']


@app.route('/')
@app.route('/login_page')
def login_page():
    return render_template('login.html')


@app.route('/user_page', methods=['post'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        if login_ == login and password == password_:
            status = '__online__'
            random.shuffle(all_user_foto)
            random_status = {}
            for i in range(random.randint(1, 8)):
                random_status[i] = random.choice(all_user_foto)
            return render_template('welcome.html', login=login, status=status, all_user_foto=all_user_foto,
                                   random_status=random_status)
        return redirect(url_for('login_page'))


@app.route('/exit', methods=['get'])
def exit_log():
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(debug=True)
