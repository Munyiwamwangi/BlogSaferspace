import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename) #throwing the variable name. tutorial 7, min30
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

#Installed Pillow for image resizing
	output_size =(125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
		sender = 'noreply@demo.com', 
		recipients = [user.email] )
	msg.body = '''To reset you password, visit;
	{url_for('users.reset_token', token = token, _external = True) }

	If yoy did not make this request, ignore this email and no changes will be made

	'''
	mail.send(msg)

#_external = True is in order to get relative url rather than absolute url.