import re


#helper functions to validate data
def validate_content(content):
	return True if not content.isspace() and content else False

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validate_username(username):
	return USER_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def validate_password(password):
	return PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def validate_email(email):
	return (not email) or EMAIL_RE.match(email) 