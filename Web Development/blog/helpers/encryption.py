import random
import string
import hashlib
 

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()

    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)


def valid_pw(name, pw, h):
    salt = h.split('|')[1]
    return make_pw_hash(name, pw, salt) == h


def make_user_cookie_hash(user_id, name, salt=None):
    if not salt:
        salt = make_salt()

    h = hashlib.sha256(user_id + name + salt).hexdigest()
    return '%s|%s|%s' % (user_id, h, salt)

def validate_user_cookie(user_id, name, h):
	salt = h.split('|')[2]
	return make_user_cookie_hash(user_id, name, salt) == h

