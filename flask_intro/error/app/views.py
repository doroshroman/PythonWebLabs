from flask import render_template
from app import app


@app.route('/')
def index():
	data = 'Hello' 
	return data


@app.route('/hi')
def to_html():
	data = {'name': "IPZ", 'surname': "41"} 
	return render_template('index.html', **data)