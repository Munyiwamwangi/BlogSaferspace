#!/usr/bin/env python

from app import create_app

'''
RECREATING THE APP VARIABLE 
HERE MAKES IT REUSABLE AS USED BELOW; RUNNING THE APP
'''
app = create_app()


if __name__ == '__main__':
	app.run(debug=True)