from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required,  current_user
from flask_sqlalchemy import SQLAlchemy
#from config import DevConfig

from app.forms import EditProfileForm, LoginForm, PlanetParamsForm, CamQueryForm, RegistrationForm
from app.models import Planet, User
from app import app, db
from exoplex.exoplex import run


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

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
    user = {}
    posts = []
    return render_template("blog.html", title='Home', user=user, posts=posts)

@app.route('/images', methods=["GET"])
@login_required
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
        # create a planet based only on fe,mg,si,o and mass. Store all these params and
        # the resulting radius in the app database
        planet_params = Planet(femg=params.femg.data, simg=params.simg.data, mass=params.mass.data)
        Planet_run = run.exoplex(femg=params.femg.data, simg=params.simg.data, mass=params.mass.data)
        mass = Planet_run[0]['mass'][-1]/5.97e24
        radius = Planet_run[0]['radius'][-1]/(6378.137*1000)
        cmf=Planet_run[0]["cmf"]
        breakpoint()
        femg, simg, _, _, _ = Planet_run[0]['bulk_ratios']
        breakpoint()
        return render_template("exoplex_result.html",
        radius=radius, mass=mass, cmf=cmf, femg='No', simg='no')
        db.session.add(planet_params)
        db.session.commit()

    return render_template("exoplex.html", titel = "ExoPlex", form = params)

#methods determine the functions accepted by this view
@app.route('/login', methods=['GET', 'POST'])
def login():
    # if user is already logged in, send them to the home route
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    # when browser sends get request, this if statement is skipped and the template is rendered
    # as per the return statement below
    if request.method == "POST":
        user = User.query.filter_by(username = form.username.data).first()
        # check password against hash in database, also validate pswd
        if (form.validate_on_submit() and
            user.check_password(form.password.data)):
            login_user(user)
            flash('Successful Login, Welcome Alejandro!', 'success')
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('images'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Sign In', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('images'))

    form = RegistrationForm()
    breakpoint()
    if form.validate_on_submit():
        user = User(username=form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, friend. You are now part of something bigger and more important than yourself.')

        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/cam_query", methods = ["GET", "POST"])
def cam_query():
    form = CamQueryForm()
    if request.method == "POST":
        if form.validate_on_submit():
            pass
        else:
            flash('you messed something up. Make sure all fields are filled', 'danger')

    return render_template("cam_query.html", title="Security Video", form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    """
    simple page for users to check out their profile and make edits
    """
    user = User.query.filter_by(username=username).first_or_404()

    return render_template("user.html", user = user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)