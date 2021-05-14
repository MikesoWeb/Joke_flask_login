import os, random
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from config_one import *

all_user_foto = ['static/img/' + i for i in os.listdir('static/img') if i != 'user_foto.jpg']


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = [User(id=1, username='Anthony', password='password'), User(id=2, username='Becca', password='secret'),
         User(id=3, username='Mike', password='12345')]
print(users)
app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        # print(g.user)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = [x for x in users if x.username == username][0]
            print(user)
            if user.username == username and user.password == password:
                session['user_id'] = user.id
                print(user.username)
                return redirect(url_for('profile'))
            flash('Пароль не верный!', category='attention')

        except IndexError:
            flash('Пользователь не найден!', category='error')

            print('It`s wrong!')

    return render_template('login.html')


@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))
    status = '__online__'
    random.shuffle(all_user_foto)
    random_status = {}
    for i in range(random.randint(1, 8)):
        random_status[i] = random.choice(all_user_foto)
    return render_template('profile.html', status=status, all_user_foto=all_user_foto,
                           random_status=random_status)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
