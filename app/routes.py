from flask import render_template, flash, redirect
#from config import DevConfig
from app.forms import LoginForm



from app import app

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/exoplex')
def exoplex():
    return render_template('exoplex.html')


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/blog')
    return render_template('login.html', title='Sign In', form=form)

if __name__ == '__main__':
    app.run()