from flask_login import LoginManager, login_user, login_required, logout_user
from flask import Flask, redirect, render_template
from data import db_session
from data.users import User
from forms.loginform import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '9vTgySlnihdzBGrf'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    db_sess = db_session.create_session()
    print(user_id)
    return db_sess.query(User).get(user_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            print(form.remember_me.data)
            login_user(user, remember=form.remember_me.data)
            return redirect("/authorized")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/authorized', methods=['GET', 'POST'])
def main():
    return render_template('authorized.html')


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
