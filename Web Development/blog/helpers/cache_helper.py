import logging

#memcache
from google.appengine.api import memcache

#import models
from blog_model import BlogPosts

#import appengine db methods for Model use
from google.appengine.ext import db


def get_latest_postings(update = False):

	key = 'latest_postings'
	blog_postings = memcache.get(key)

	if blog_postings == None or update:
		#show error in the console 
		logging.error('DB POSTING QUERY')

		blog_postings = db.GqlQuery("SELECT * "
								"FROM BlogPosts "
								"ORDER BY created DESC LIMIT 10")

		#datastore query is executed
		blog_postings = list(blog_postings)				

		memcache.set(key, blog_postings)

	return blog_postings

def get_blog_post(post_id):
	key = post_id
	blog_post = memcache.get(key)

	if blog_post == None:
		#show error in the console 
		logging.error('DB ID QUERY')
		blog_post = BlogPosts.get_by_id(int(post_id))

		#datastore query is executed
		blog_post = blog_post			

		memcache.set(key, blog_post)

	return blog_post

