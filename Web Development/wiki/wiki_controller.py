import webapp2
import jinja2
import os
import random
import string
import time
import json

#import models
from wiki_model import WikiPost, User

#import helper functions
from helpers.validations import validate_content, validate_username, validate_password, validate_email
from helpers.encryption import check_secure_val, make_secure_val
from helpers.cache_helper import get_cached_data, cache_data, reset_cache

#Setup view directory for Jinja template engine
template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
																autoescape = True)


#http request handlers
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		params['user'] = self.user
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def render_json(self, d):
		json_txt = json.dumps(d)
		self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
		self.write(json_txt)

	def set_secure_cookie(self, name, val):
		cookie_val = make_secure_val(val)
		self.response.headers.add_header(
			'Set-Cookie',
			'%s=%s; Path=/' % (name, cookie_val))

	def read_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		return cookie_val and check_secure_val(cookie_val)

	def login(self, user):
		self.set_secure_cookie('user_id', str(user.key().id()))

	def logout(self):
		self.response.delete_cookie('user_id')

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.read_secure_cookie('user_id')
		self.user = uid and User.by_id(int(uid))

		if self.request.url.endswith('.json'):
			self.format = 'json'
		else:
			self.format = 'html'


class WikiPageHandler(Handler):
	def get(self, url):
		self.render('wiki_page.html')


class SignupHandler(Handler):
	def get(self):
		self.render('signup.html')

	def post(self):
		have_error = False
		self.username = self.request.get('username')
		self.password = self.request.get('password')
		self.verify = self.request.get('verify')
		self.email = self.request.get('email')

		params = dict(username = self.username,
					  email = self.email)

		if not validate_username(self.username):
			params['error_username'] = "That's not a valid username."
			have_error = True

		if not validate_password(self.password):
			params['error_password'] = "That wasn't a valid password."
			have_error = True
		elif self.password != self.verify:
			params['error_mismatch_passwords'] = "Your passwords didn't match."
			have_error = True

		if not validate_email(self.email):
			params['error_email'] = "That's not a valid email."
			have_error = True

		if have_error:
			self.render('signup.html', **params)
		else:
			self.register()

	def register(self):
		#make sure the user doesn't already exist
		u = User.by_name(self.username)
		if u:
			msg = 'That user already exists.'
			self.render('signup-form.html', error_username = msg)
		else:
			if self.email:
				recently_add_user = User.register(self.username, self.password, self.email)
			else:
				recently_add_user = User.register(self.username, self.password)

			#save user to db and login user
			recently_add_user.put()
			self.login(recently_add_user)

			#redirect to home page
			self.redirect('/')

		

class LoginHandler(Handler):
	def get(self):
		self.render('login.html')

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')

		u = User.login(username, password)
		if u:
			self.login(u)
			self.redirect('/')
		else:
			msg = 'Invalid login'
			self.render('login.html', error = msg)


class LogoutHandler(Handler):
	def get(self):
		#path for redirection
		path = self.request.get('path')

		#logout & redirect to webpage
		self.logout()
		self.redirect('%s' % path)


class EditPageHandler(Handler):
	def get(self):
		self.response('blah')

class AboutPageHandler(Handler):
	def get(self):
		self.render('about.html')


PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/about/?', AboutPageHandler),
							   ('/signup/?', SignupHandler),
							   ('/login/?', LoginHandler),
							   ('/logout/?', LogoutHandler),
							   ('/_edit' + PAGE_RE, EditPageHandler),
							   (PAGE_RE, WikiPageHandler),
							   ],
							  debug=True)