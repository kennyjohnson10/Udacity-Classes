from google.appengine.ext import db
from helpers.encryption import make_pw_hash, valid_pw

#Blog Models
class WikiPost(db.Model):
	"""Models an individual BlogPosts entry with an subject, content, and date."""
	url_path = db.StringProperty(required = True)
	url_content = db.TextProperty(required = True)

	@classmethod
	def by_id(cls, url_id):
		return User.get_by_id(url_id)

	@classmethod
	def by_name(cls, url_path):
		wiki_post = WikiPost.all().filter('url_path =', url_path).get()
		return wiki_post

	@classmethod
	def create(cls, url_path, url_content):
		return WikiPost(url_path = url_path,
						url_content = url_content)


def users_key(group = 'default'):
	return db.Key.from_path('users', group)

class User(db.Model):
	"""Models an individual Users account with a username, password, and email."""
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.EmailProperty(required = True)

	@classmethod
	def by_id(cls, uid):
		return User.get_by_id(uid, parent = users_key())

	@classmethod
	def by_name(cls, name):
		u = User.all().filter('name =', name).get()
		return u

	@classmethod
	def register(cls, name, pw, email = None):
		pw_hash = make_pw_hash(name, pw)
		return User(parent = users_key(),
					name = name,
					pw_hash = pw_hash,
					email = email)

	@classmethod
	def login(cls, name, pw):
		u = cls.by_name(name)
		if u and valid_pw(name, pw, u.pw_hash):
			return u