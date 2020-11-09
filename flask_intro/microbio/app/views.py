from flask import render_template, redirect, flash, url_for
from app import app, db
from .forms import RegistrationForm, LoginForm
from .models import User, Post
from flask_login import current_user, login_user, logout_user, login_required

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        email = reg_form.email.data
        password = reg_form.password.data
        
        user = User(username=username, email=email, password_hash=password)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        # Make flash message
        flash(f'Account created for {user.username}', 'info')
        return redirect(url_for('login'))

    return render_template('register.html', form=reg_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            flash(f'Welcome back {user.username}', 'info')
            login_user(user)
            return redirect(url_for('account'))
        else:
            flash(f'Incorrect email or password', 'warning')
        
    return render_template('login.html', form=login_form)

@app.route('/posts', methods=['GET'])
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('show_main_page'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html')