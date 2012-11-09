import webapp2
import jinja2
import os
import random
import string
import time
import json

#xml library, used for parsing xml
from xml.dom import minidom

#import models
from blog_model import BlogPosts, Users

#import appengine db methods for Model use
from google.appengine.ext import db

#import helper functions
from helpers.validations import validate_blog_subject, validate_blog_body, validate_username, validate_password, validate_email
from helpers.encryption import make_user_cookie_hash, validate_user_cookie, make_pw_hash, valid_pw
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
		t = jinja_env.get_template(template)
		params['login_status'] = self.login_status()
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	def login_status(self):
		return self.request.cookies.get('user_id')

	def render_json(self, data):
		json_txt = json.dumps(data)
		self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
		self.write(json_txt)

	def render_xml(self, data):
		xml_txt = minidom.parseString(data)
		self.response.headers['Content-Type'] = 'text/xml; charset=UTF-8'
		self.write(xml_txt)


class BlogHandler(Handler):
	def get(self):
		blog_postings_data = get_latest_postings()
		render_time = blog_postings_data[1]

		time_since_page_generated = 'Queried %s seconds ago' % render_time
		#render page
		self.render('home.html', blog_postings = blog_postings_data[0], 
					time_since_page_generated = time_since_page_generated,
					 home_active_tab = 'active')


class NewPostHandler(Handler):
	def get(self):
		self.render('newpost.html', newpost_active_tab = 'active')

	def post(self):
		blog_subject = self.request.get('subject')
		blog_body = self.request.get('content')

		valid_subject = validate_blog_subject(blog_subject)
		valid_body = validate_blog_body(blog_body)

		if not (valid_subject and valid_body): 
			error_subject = ''
			error_content = ''

			if not valid_subject:
				error_subject = 'Please add a valid subject.'

			if not valid_body:
				error_content = 'Please add valid content.'

			self.render('newpost.html', subject = blog_subject, 
										content = blog_body,
										error_subject = error_subject,
										error_content = error_content,
										active_tab = 'active')
		else:
			blog_posting = BlogPosts(subject=blog_subject, content=blog_body)
			blog_posting.put()
			permalink_id = str(blog_posting.key().id())

			#update memcache and redirect to permalink
			get_latest_postings(True)
			self.response.headers.add_header('Set-Cookie', 
								'render_time=; Path=/blog')
			self.redirect('/blog/'+ permalink_id)

class PermalinkHandler(Handler):
	def get(self, post_id):
		blog_post = get_blog_post(post_id)
		render_time = blog_post[1]

		time_since_page_generated = 'queried %s seconds ago' % render_time
		
		#render page
		self.render('permalink.html', blog_subject = blog_post[0].subject,
									blog_datetime = blog_post[0].created,
									blog_content = blog_post[0].content,
									perma_link_title = post_id,
									time_since_page_generated = time_since_page_generated)


class SignupHandler(Handler):
	def get(self):
		self.render('signup.html', not_relevant = True)

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')

		valid_username = validate_username(username)
		valid_password = validate_password(password) and validate_password(verify)
		mismatch_passwords = password == verify
		valid_email = validate_email(email)

		#query for user data to check for duplicate users in db
		
		q = Users.all()
		q.filter("username =", username)
		user_result = q.get()
		

		if user_result or not (valid_username and valid_password 
					and mismatch_passwords and valid_email):
			error_username = ''
			error_password = ''
			error_mismatch_passwords = ''
			error_email = ''

			if not valid_username or user_result:
				error_username = "That's not a valid username."

			if not valid_password:
				error_password = "That's not a valid password."
			elif not mismatch_passwords:
				error_mismatch_passwords = "Your passwords didn't match."

			if (not valid_email) and email != '':
				error_email = "That's not a valid email."

			self.render('signup.html', error_username = error_username,
										error_password = error_password,
										error_mismatch_passwords = error_mismatch_passwords,
										error_email = error_email,
										username = username,
										email = email)

		else:
			#hash password
			hashed_password = make_pw_hash(username, password)

			if email:
				recently_added_user = Users(username = username, 
									password = hashed_password, 
									email = email)
			else:
				recently_added_user = Users(username = username, 
									password = hashed_password, 
									email = 'company_email@company.com')
			recently_added_user.put()

			#make cookie hash
			user_id = str(recently_added_user.key().id())
			cookie_data = make_user_cookie_hash(user_id,  username)
			
			self.response.headers.add_header('Set-Cookie', 
									'user_id=%s; Path=/blog' % cookie_data)
			self.redirect('/blog/welcome')


class WelcomeHandler(Handler):
	def get(self):
		#get cookie data
		hash_data = self.request.cookies.get('user_id')

		if hash_data:
			user_id = hash_data.split('|')[0]

			#make call to db to get username using user_id
			user = Users.get_by_id(int(user_id))

			#check cookie for user information and render html
			if validate_user_cookie(user_id, user.username, hash_data):
				self.render('welcome.html', name = user.username, 
											user_logged_in = True)

		else:
			self.redirect('/blog/signup')


class LoginHandler(Handler):
	def get(self):
		self.render('login.html', not_relevant = True)

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')

		#query for user data 
		q = Users.all()
		q.filter("username =", username)
		user_result = q.get()

		if user_result and validate_password(password) and validate_username(username):
			if user_result.username == username and valid_pw(username, password, user_result.password):
				user_id = str(user_result.key().id())
				cookie_data = make_user_cookie_hash(user_id,  username)
				
				self.response.headers.add_header('Set-Cookie', 
										'user_id=%s; Path=/' % cookie_data)
				self.redirect('/blog/welcome')
		
		self.render('login.html', error = "Invalid login.", 
								  username = username, 
								  not_relevant = True)


class LogoutHandler(Handler):
	def get(self):
		self.response.delete_cookie('user_id')
		self.redirect('/blog')

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


app = webapp2.WSGIApplication([('/blog/?', BlogHandler),
								('/blog/newpost/?', NewPostHandler),
								('/blog/(\\d+)/?', PermalinkHandler),
								('/blog/signup/?', SignupHandler),
								('/blog/welcome/?', WelcomeHandler),
								('/blog/login/?', LoginHandler),
								('/blog/logout/?', LogoutHandler),
								('/blog/(\\d+)/?\\.json/?', PermalinkAPIHandler),
								('/blog/?\\.json/?', BlogAPIHandler),
								('/blog/flush/?', CacheFlushHandler),
								('/blog/about/?', AboutHandler),],
								debug=True)