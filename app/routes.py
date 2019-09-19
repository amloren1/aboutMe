from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
#from config import DevConfig
from app.forms import LoginForm, PlanetParamsForm
from app.models import Planet, User
from app import app, db



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route("/blog")
def blog():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("blog.html", title='Home', user=user, posts=posts)

@app.route('/images', methods=["GET"])
def images():
    return render_template('images.html')


@app.route('/exoplex', methods=['GET', 'POST'])
def exoplex():
    def check_login(user, password):
        if user == "admin" and password == "dakine":
            return True
        else:
            return False

    params = PlanetParamsForm()
    if params.validate_on_submit():
        planet = Planet(femg=params.femg.data, simg=params.simg.data, mass=params.mass.data)
        db.session.add(planet)
        db.session.commit()
    return render_template("exoplex.html", titel = "ExoPlex", form = params)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(username = form.username.data).first()
        if (form.validate_on_submit() and
            user.password == form.password.data):
            login_user(user)
            flash('Successful Login, Welcome Alejandro!', 'success')
            return redirect(url_for('images'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Sign In', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

