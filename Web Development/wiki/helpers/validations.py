import re


#helper functions to validate data
def validate_blog_subject(blog_subject):
	return True if not blog_subject.isspace() and blog_subject else False

def validate_blog_body(blog_body):
	return True if not blog_body.isspace() and blog_body else False

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validate_username(username):
	return USER_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def validate_password(password):
	return PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def validate_email(email):
	return (not email) or EMAIL_RE.match(email) 