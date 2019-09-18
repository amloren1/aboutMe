from flask import render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
#from config import DevConfig
from app.forms import LoginForm, PlanetParamsForm

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

    return render_template("exoplex.html", titel = "ExoPlex", form = params)

@app.route('/login', methods=['GET', 'POST'])
def login():
    def check_login(user, password):
        if user == "admin" and password == "dakine":
            return True
        else:
            return False

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if check_login(form.username.data, form.password.data):
                flash(f'Successful Login, Welcome Admin: {form.username.data}', 'success')
        #TODO: validate as admin
                return redirect(url_for('images'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Sign In', form=form)

if __name__ == '__main__':
    app.run()