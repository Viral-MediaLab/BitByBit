#!/usr/bin/python
'''
BitByBit Restful API
'''
import json
import time

import urllib, urllib2, Cookie
import hashlib

from flask import Flask, request, abort, redirect, Response, jsonify
from flask.ext.restful import Resource, Api, reqparse

from db import MongoInstance
from bson.objectid import ObjectId

application = Flask(__name__)
api = Api(application)

PORT = 8888

############################
# Once domains are set, we need to update the following to only allow access to bitbybit.me 
############################
@application.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """
    if request.method == 'OPTIONS':
        resp = application.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        h['Access-Control-Allow-Origin'] = request.headers['Origin']# Allow the origin which made the XHR
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']# Allow the actual method
        h['Access-Control-Max-Age'] = "10"# Allow for 10 seconds

        if headers is not None:        # We also keep current headers 
            h['Access-Control-Allow-Headers'] = headers

        return resp

@application.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """
    h = resp.headers
    if request.method != 'OPTIONS' and 'Origin' in request.headers: # Allow crossdomain for other HTTP Verbs
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        
    h['Access-Control-Allow-Credentials'] = 'true'
    return resp




############################
# Endpoint Specifications
############################

############################
# publicTest
############################
publicGetParser = reqparse.RequestParser()
publicGetParser.add_argument('q', type=str, required=True)
class Public(Resource):
	def get(self):
		args = publicGetParser.parse_args()
		q = args.get('q')
		# cookies = dict([e.split('=') for e in request.headers['Cookie'].replace(' ', '').split(';')])
		# print cookies
		try:
			cookie = request.headers['Cookie']
		except:
			cookie = "No Cookies!"
		return "You just did the dang public, sir! You said " + q + " !!!! cookies: " + cookie
		# return MongoInstance.getPublic(uID)
api.add_resource(Public, '/api/public/test')

############################
# privateTest
############################
privateGetParser = reqparse.RequestParser()
privateGetParser.add_argument('q', type=str, required=True)
class Private(Resource):
	def get(self):
		args = privateGetParser.parse_args()
		q = args.get('q')
		# cookies = dict([e.split('=') for e in request.headers['Cookie'].replace(' ', '').split(';')])
		# print cookies
		try:
			cookie = request.headers['Cookie']
		except:
			cookie = "No Cookies!"
		return "Awww Private in this biz! You said " + q + " !!!! cookies: " + cookie
		# return MongoInstance.getPublic(uID)
api.add_resource(Private, '/api/private/test')



############################
# Goal
############################
goalGetParser = reqparse.RequestParser()
# goalGetParser.add_argument('uID', type=str, required=True)

goalPostParser = reqparse.RequestParser()
# goalPostParser.add_argument('uID', type=str, required=True)
goalPostParser.add_argument('goal', type=str, required=True)

goalDeleteParser = reqparse.RequestParser()
goalDeleteParser.add_argument('uID', type=str, required=True)

class Goal(Resource):
	def get(self):
		args = goalGetParser.parse_args()
		# uID = args.get('uID')
		try:
			cookie = request.headers['Cookie']
			req = urllib2.Request('http://www.media.mit.edu/login/valid/index.html')
			req.add_header('Cookie', cookie)
			r = urllib2.urlopen(req)
			# print r.read()
			if r.read()[:4]=='true':
				# print 'yep'
				c = Cookie.SimpleCookie()
				# print hcook
				c.load(str(cookie))
				mlCookie = c['MediaLabUser'].value
				user = urllib.unquote(mlCookie).split(';')[0]
				hash_object = hashlib.sha1(user)
				uID = hash_object.hexdigest()
				

				# = urllib.unquote(mlCookie).split(';')[5]
				# print user
				# print uID

				if len(user.split('@media.mit.edu')) == 2:
					username = user.split('@media.mit.edu')[0]
				else:
					username = user

				# print username

				try:
					req2 = urllib2.Request('http://data.media.mit.edu/spm/contacts/json?username='+username)
					# req2.add_header('Cookie', cookie)
					r2 = urllib2.urlopen(req2)
					x = r2.read()
					name = json.loads(x)['profile']['first_name']
					image = json.loads(x)['profile']['picture_url']
				except:
					name = 'You'
					image = 'images/face.jpg'

				MongoInstance.addUserData(uID,user,name,image)
				return {'name':name, 'image':image, 'goal':MongoInstance.getGoal(uID)}
			else:
				return 'redirect'
				# return redirect("http://www.media.mit.edu/login?destination=bitxbit.media.mit.edu%2Fteam&previous=bitxbit.media.mit.edu", code=302)
			
		except:
			cookie = "No Cookies!"
			return 'redirect'
			# return redirect("http://www.media.mit.edu/login?destination=http%3A%2F%2Fbitxbit.media.mit.edu%2Fteam&previous=http%3A%2F%2Fbitxbit.media.mit.edu", code=302)
		# return cookie
		
	def post(self):
		args = goalPostParser.parse_args()
		# uID = args.get('uID')
		goal = args.get('goal')
		# print goal
		
		try:
			cookie = request.headers['Cookie']
			req = urllib2.Request('http://www.media.mit.edu/login/valid/index.html')
			req.add_header('Cookie', cookie)
			r = urllib2.urlopen(req)
			# print r.read()
			if r.read()[:4]=='true':
				# print 'yep'
				c = Cookie.SimpleCookie()
				# print hcook
				c.load(str(cookie))
				mlCookie = c['MediaLabUser'].value
				user = urllib.unquote(mlCookie).split(';')[0]
				hash_object = hashlib.sha1(user)
				uID = hash_object.hexdigest()

				# print user
				# print uID

				# if len(user.split('@media.mit.edu')) == 2:
				# 	username = user.split('@media.mit.edu')[0]
				# else:
				# 	username = user

				# print username

				
				# req2 = urllib2.Request('http://data.media.mit.edu/spm/contacts/json?username='+username)
				# # req2.add_header('Cookie', cookie)
				# r2 = urllib2.urlopen(req2)
				# x = r2.read()
				# name = json.loads(x)['profile']['first_name']
				# image = json.loads(x)['profile']['picture_url']
				return MongoInstance.postGoal(uID, goal)
			else:
				return 'redirect'
				# return redirect("http://www.media.mit.edu/login?destination=bitxbit.media.mit.edu%2Fteam&previous=bitxbit.media.mit.edu", code=302)
			
		except:
			cookie = "No Cookies!"
			return 'redirect'
			# return redirect("http://www.media.mit.edu/login?destination=http%3A%2F%2Fbitxbit.media.mit.edu%2Fteam&previous=http%3A%2F%2Fbitxbit.media.mit.edu", code=302)
		
	def delete(self):
		args = goalDeleteParser.parse_args()
		uID = args.get('uID')
		return MongoInstance.deleteGoal(uID)
api.add_resource(Goal, '/api/private/goal')


############################
# User
############################
userGetParser = reqparse.RequestParser()
userGetParser.add_argument('uID', type=str, required=True)

userPostParser = reqparse.RequestParser()
userPostParser.add_argument('uID', type=str, required=True)

userDeleteParser = reqparse.RequestParser()
userDeleteParser.add_argument('uID', type=str, required=True)

class User(Resource):
	def get(self):
		args = userGetParser.parse_args()
		uID = args.get('uID')
		return MongoInstance.getUser(uID)
	def post(self):
		args = userPostParser.parse_args()
		uID = args.get('uID')
		return MongoInstance.postUser(uID)
	def delete(self):
		args = userDeleteParser.parse_args()
		uID = args.get('uID') 
		return MongoInstance.deleteUser(uID)
api.add_resource(User, '/api/user')

############################
# Get All Users
############################
# userGetParser = reqparse.RequestParser()
# userGetParser.add_argument('uID', type=str, required=True)

class AllUsers(Resource):
	def get(self):
		return MongoInstance.allUsers()
api.add_resource(AllUsers, '/api/allusers')



if __name__ == '__main__':
    # application.run(host = '0.0.0.0', debug=True)
    # application.run(host = 'localhost.media.mit.edu', debug=True)
    application.run(host = 'localhost', debug=True)
    #application.run(debug="true", port=PORT)
