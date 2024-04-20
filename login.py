from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, redirect, render_template
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.loginform import LoginForm
from forms.job import JobsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '9vTgySlnihdzBGrf'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/authorized')
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
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    query = db_sess.query(User)
    crew_members = []
    for user in db_sess.query(User).all():
        # crew_members.append((user.surname, user.name))
        crew_members.append(user.name)

    return render_template('jobs.html', jobs=jobs, crew=crew_members)


@app.route('/add_jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.team_leader = form.team_leader.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/authorized')
    return render_template('add_jobs.html', title='Добавление новости',
                           form=form)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
