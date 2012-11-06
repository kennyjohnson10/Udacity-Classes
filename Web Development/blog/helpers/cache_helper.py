import logging

#memcache
from google.appengine.api import memcache

#import appengine db methods for Model use
from google.appengine.ext import db


def latest_postings(, update = False):

	key = 'latest_postings'
	blog_postings = memcache.get(key)

	if blog_postings == None or update:
		#show error in the console 
		logging.error('DB QUERY')

		blog_postings = db.GqlQuery("SELECT * "
								"FROM BlogPosts "
								"ORDER BY created DESC LIMIT 10")

		#datastore query is executed
		blog_postings = list(blog_postings)				

		memcache.set(key, blog_postings)

	return blog_postings

def permalink_caching(self):
	pass