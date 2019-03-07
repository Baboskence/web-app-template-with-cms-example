#ASYNC
from gevent import monkey
monkey.patch_all()
from bottle import run

#***DEFINE PAGE ROUTES***
import src.definePages

#***RUN SERVER***
#TURN OFF RELOADER AND DEBUG FOR PRODUCTION
#FOR SSL/TSL SUPPORT: certfile='server.crt', keyfile='server.key'
run(host='localhost', 
	port=3000, 
	debug=True, 
	reloader=True, 
	server='gevent')
	
	
"""
TODO:
	-auth_basic log out
	-page from json
	-page group to admin
	-better /admin ui(responsive)
"""