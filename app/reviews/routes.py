from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from app import db
from app.models import Review, User, Post
from app.reviews.forms import ReviewForm


#instatntiating the blueprint
reviews = Blueprint('reviews',__name__)

#POSTS
@reviews.route("/review/new/<int:id>", methods=['GET','POST'])
def new_review(id):
	form = ReviewForm()
	if form.validate_on_submit():
		review_id=id		
		user = User.query.filter_by(id = id).first_or_404()
		posts = Post.query.filter_by(user = user)\
		.order_by(Post.date_posted.desc())
		reviews = Review(name = form.name.data, content = form.content.data)
		db.session.add(reviews)
		db.session.commit()
		flash('you have commented succesfully', 'success')
		return render_template('review.html', reviews = reviews, post_id=id)
	return render_template('create_review.html', title = 'New Review', form = form, id=id,legend = 'New Review')


@reviews.route("/review/<int:post_id>")
def review(post_id):
	review = Review.query.get_or_404(post_id)
	return render_template('review.html', title = review.name, review = review)

#UPDATE REVIEW
@reviews.route("/review/<int:review_id>/update", methods=['GET','POST'])
@login_required
def update_review(review_id):
	review = Review.query.get_or_404(review_id)
	if review.user != current_user:
		abort(403)
	form = ReviewForm()
	if form.validate_on_submit():
		review.name =  form.name.data
		review.content= form.content.data
		db.session.commit()
		flash('Review update successfull', 'success')
		return redirect(url_for('reviews.review', review_id = id))
	elif request.method == 'GET':
		form.name.data = review.name
		form.content.data = review.content
	return render_template('create_review.html', title = 'Update Review',
		form = form, legend = 'Update Review')


#DELETE REVIEW
@reviews.route("/review/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_review(post_id):
	review = Review.query.get_or_404(post_id)
	if review.user != current_user:
		abort(403)
	db.session.delete(review)
	db.session.commit()
	flash('Review deleted', 'success')
	return redirect(url_for('main.home'))
