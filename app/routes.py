from flask import Flask, render_template
#from config import DevConfig


from app import app

@app.route('/')
def home():
    return "Here" #render_template('../templates/home.html')

@app.route('/resume')
def resume():
    return "There" #render_template('../templates/resume.html')

@app.route('/exoplex')
def exoplex():
    return "Bad Gateway"#render_template('../templates/exoplex.html')

if __name__ == '__main__':
    app.run()