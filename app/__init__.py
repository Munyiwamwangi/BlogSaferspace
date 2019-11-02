from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

#db instance
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
#we want to tie users to login so that they can only access user account infof if they are logged in
login_manager.login_view = 'users.login'
#login_message_category is a bootstrap class
login_manager.login_message_category = 'info'
#setting up mail 
#initializing the mailing extension 
mail = Mail()


'''
WE MOVE CREATION OF THE APP INTANCE INTO A FUNCTION
SO AS TO CREATE DIFFERENT INSTANCES OF OUR APP
WE ARE MOVING EVERYTHING INTO THIS FUNCTION
WE MOVE BLUEPRINTS INTO THE FUNCTION
'''
def create_app(config_class=Config):
	
	#APP CREATION COMES FIRST
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)

	with app.app_context():
		db.create_all()

	'''
	THEN RUN THE APP INTO EVERY OF THESE, 
	PASS IN THE APP, AND
	AND RETURN THE APP IN THE LAST LINE BELOW
	'''
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)



	#IMPORTING ROUTES SO AS TO REGISTER THE INITIALIZED BLUEPRINTS
	from app.main.routes import main
	from app.posts.routes import posts
	from app.users.routes import users
	from app.reviews.routes import reviews
	from app.errors.handlers import errors

	#REGISTERING THE  BLUEPRINTS NOW
	app.register_blueprint(main)
	app.register_blueprint(posts)
	app.register_blueprint(users)
	app.register_blueprint(reviews)
	app.register_blueprint(errors)


	return app