from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ReviewForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	content = TextAreaField('Comment', validators=[DataRequired()])
	submit = SubmitField('Post Comment')