import os #FOR SETTING EVIRONMENT VARIABLES

class Config:
	SECRET_KEY = 'de74e7b0fad76d362bfd1fcd0c0fd885'
	#init db
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT =  587
	MAIL_USE_TLS = True
	MAIL_USERNAME =  os.environ.get('EMAIL_USER')
	MAIL_PASSWORD=  os.environ.get('EMAIL_PASS')