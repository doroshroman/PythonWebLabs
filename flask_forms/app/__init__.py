from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'natusvincere'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Le4kdkZAAAAAJtGX-B82T6Y7bwSAB13LG4vX1oy'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Le4kdkZAAAAAP5ipwGOrxHULATZ37nfcefZ4w1P'
app.config['TESTING'] = True

from app import views