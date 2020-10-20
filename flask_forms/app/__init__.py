from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'natusvincere'
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('RECAPTCHA_PUBLIC_KEY', None)
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('RECAPTCHA_PRIVATE_KEY', None)
app.config['TESTING'] = True

from app import views