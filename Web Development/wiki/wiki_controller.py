import webapp2
import jinja2
import os
import random
import string
import time
import json

#import models
from blog_model import BlogPosts, Users

#import appengine db methods for Model use
from google.appengine.ext import db

#import helper functions
from helpers.validations import validate_blog_subject, validate_blog_body, validate_username, validate_password, validate_email
from helpers.encryption import check_secure_val
from helpers.cache_helper import get_latest_postings, get_blog_post, reset_cache

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
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.read_secure_cookie('user_id')
		self.user = uid and User.by_id(int(uid))

		if self.request.url.endswith('.json'):
			self.format = 'json'
		else:
			self.format = 'html'


class PermalinkAPIHandler(Handler):
	def get(self, post_id):
		blog_post = BlogPosts.get_by_id(int(post_id))

		if blog_post:
			self.response.headers['Content-Type'] = 'application/json'
			self.write(json.dumps({'contents': str(blog_post.content),
									'created': time.strftime(str(blog_post.created)),
									'subject': str(blog_post.subject)}))
		else:
			self.render('404.html')

class BlogAPIHandler(Handler):
	def get(self):
		q = BlogPosts.all()
		q.order("-created")

		blog_listings = []
		for blog_post in q.run(limit=10):
			if blog_post:
				blog_listings.append({'contents': str(blog_post.content),
									  'created': time.strftime(str(blog_post.created)),
									  'subject': str(blog_post.subject)})

		if blog_listings:
			self.response.headers['Content-Type'] = 'application/json'
			self.write(json.dumps(blog_listings))
		else:
			self.render('404.html')


class CacheFlushHandler(Handler):
	def get(self):
		#flush the cache and redirect
		reset_cache()
		self.redirect('/blog')


class AboutHandler(Handler):
	def get(self):
		self.render('about.html')


PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/signup', SignupHandler),
							   ('/login', LoginHandler),
							   ('/logout', LogoutHanlder),
							   ('/_edit' + PAGE_RE, EditPageHandler),
							   (PAGE_RE, WikiPage),
							   ],
							  debug=True)