from flask import render_template, redirect, flash, url_for, request
from app import app, db
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, CreatePostForm, UpdatePostForm
from .models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import os
import secrets
from PIL import Image
from datetime import datetime

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
    if current_user.is_authenticated:
        return redirect(url_for('show_main_page'))
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
        return redirect(url_for('show_main_page'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        remember = login_form.remember.data

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            flash(f'Welcome back {user.username}', 'info')
            login_user(user, remember=remember)
            next_url = request.args.get('next')
            
            if not next_url or url_parse(next_url).netloc != '':
                next_url = url_for('show_main_page')
            return redirect(next_url)

        else:
            flash(f'Incorrect email or password', 'warning')
        
    return render_template('login.html', form=login_form)

@app.route('/posts/', methods=['GET'])
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('show_main_page'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file 
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
        form.password.data = current_user.password_hash

    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image=image_file, form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    name, ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (120, 120)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/post/new/', methods=['GET', 'POST'])
@login_required
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data

        post = Post(title=title, body=body, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Nice post, but you can better', 'success')
        return redirect(url_for('posts'))

    return render_template('create_post.html', form=form)


@app.route('/posts/<int:post_id>/', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/<int:post_id>/update/', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.timestamp = datetime.utcnow()
        db.session.commit()
        flash('I like it better now!', 'success')
        return redirect(url_for('update_post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body

    return render_template('update_post.html', form=form, post=post)


@app.route('/posts/delete/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)
    title = post.title
    db.session.delete(post)
    db.session.commit()
    flash(f'Post {title} was deleted!', 'success')
    return redirect(url_for('posts'))