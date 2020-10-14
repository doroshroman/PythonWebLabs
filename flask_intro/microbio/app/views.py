from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def show_main_page():
	return render_template('index.html')

@app.route('/bio')
def show_bio():
    return render_template('bio.html')

@app.route('/hobbies')
def show_hobbies():
    return render_template('hobbies.html')
