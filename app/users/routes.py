import os

from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message

import app
from app import bcrypt, db, mail
from app.models import Post, User
from app.users.forms import (LoginForm, RegistrationForm, RequestResetForm,
                             ResetPasswordForm, UpdateAccountForm)
from app.users.utils import save_picture, send_reset_email

#instatntiating the blueprint
users = Blueprint('users',__name__)

@users.route("/register/", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()

		flash(f'Account created for {form.username.data}. You can now login', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title = 'Register', form = form)

@users.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember = form.remember.data)
			next_page = request.args.get('next')
			#redirect to the next page if it exists, else render home
			#if there is not a next page, always render home
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash(f'Login Unsuccesfull. Please check email and password.', 'danger')
	return render_template('login.html', title = 'Login', form = form)


#LOGOUT USER
@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.home'))

	#ACCOUNT
@users.route("/account", methods=['GET','POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect (url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title = 'Account', 
		image_file = image_file, form=form)


#USERS TO SEE THEIR POSTS WHEN CLICK THEIR USERNAME

@users.route("/user/<string:username>")
def user_posts(username):
	#PAGINATION
	page = request.args.get('page', 1, type = int)
	user = User.query.filter_by(username = username).first_or_404()
	posts = Post.query.filter_by(user = user)\
		.order_by(Post.date_posted.desc())\
		.paginate(page = page, per_page = 5)
	return render_template('user_posts.html', posts=posts, user = user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
