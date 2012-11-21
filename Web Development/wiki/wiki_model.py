from google.appengine.ext import db

#Blog Models
class WikiPost(db.Model):
	"""Models an individual BlogPosts entry with an subject, content, and date."""
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)


class User(db.Model):
	"""Models an individual Users account with a username, password, and email."""
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.EmailProperty()

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