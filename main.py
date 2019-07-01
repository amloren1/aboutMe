from flask import Flask, render_template
from config import DevConfig


app = Flask(__name__)
app.config.from_object(DevConfig)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/exoplex')
def exoplex():
    return render_template('exoplex.html')

if __name__ == '__main__':
    app.run()