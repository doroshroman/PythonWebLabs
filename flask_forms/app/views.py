from flask import render_template
from app import app
from .forms import LoginForm

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    form = LoginForm()

    if form.validate_on_submit():
        return f'<h1>The username is: {form.username.data}. The password is: {form.password.data}</h1>'
    return render_template('login_form.html', form=form)