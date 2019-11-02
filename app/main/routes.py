from flask import render_template, request, Blueprint, redirect
from app.models import Post, Review, User
import json
import requests
#initlialize blueprint
main = Blueprint('main',__name__)


@main.route("/")
@main.route("/home")
def home():

	#PAGINATION
	page = request.args.get('page', 1, type = int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)
	# reviews = Review.query.order_by(Review.date_posted.desc()).paginate(page = page, per_page = 5)
	return render_template('home.html', posts=posts)

@main.route("/about")
def about():
	return render_template ('about.html', title='About')



@main.route("/quotes")
def quotes():
	random = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
	return render_template('index.html', random=random)