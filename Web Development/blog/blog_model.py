from google.appengine.ext import db

#Blog Models
class BlogPosts(db.Model):
	"""Models an individual BlogPosts entry with an subject, content, and date."""
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	datetime = db.DateTimeProperty(auto_now_add = True)


class Users(db.Model):
	"""Models an individual Users account with a username, password, and email."""
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.EmailProperty(required = True)

