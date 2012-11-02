import webapp2
import cgi
import re

form = '''
<!DOCTYPE html>
<html>
<head>
<title>My ROT13 Site</title>
</head>
<body>
<h2>Signup</h2>
		<form method="post">
			<label>
				Username
				<input type="text" value="%(username)s" name="username">
				<span style="color:red;">%(error_username)s</span>
			</label>
			<br>
			<label>
				Password
				<input type="password" name="password">
				<span style="color:red;">%(error_password)s</span>
			</label>
			<br>
			<label>
				Verify Password
				<input type="password" name="verify">
				<span style="color:red;">%(error_mismatch_passwords)s</span>
			</label>
			<br>
			<label>
				Email (optional)
				<input type="text" value="%(email)s" name="email">
				<span style="color:red;">%(error_email)s</span>
			</label>
			<br>
			<input type="submit">
		</form>
</body>
</html>
		'''


def escape_html(s):
	return cgi.escape(s, quote = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validate_username(username):
	return USER_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def validate_password(password):
	return PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def validate_email(email):
	return (not email) or EMAIL_RE.match(email) 


class MainPage(webapp2.RequestHandler):
	def write_form(self, error_username="", error_password="", 
					error_mismatch_passwords="", error_email="", username="", email=""):
		self.response.out.write(form % {'error_username': escape_html(error_username),
										'error_password': escape_html(error_password), 
										'error_mismatch_passwords': escape_html(error_mismatch_passwords),
										'error_email': escape_html(error_email),
										'username': escape_html(username),
										'email': escape_html(email)})

	def get(self):
		self.write_form()

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')

		valid_username = validate_username(username)
		valid_password = validate_password(password) and validate_password(verify)
		mismatch_passwords = password == verify
		valid_email = validate_email(email)

		if not (valid_username and valid_password and mismatch_passwords and valid_email):
			errors = [valid_username, valid_password, mismatch_passwords, valid_email]

			error_username = ''
			error_password = ''
			error_mismatch_passwords = ''
			error_email = ''

			for error in errors:
				if not valid_username:
					error_username = "That's not a valid username."

				if not valid_password:
					error_password = "That wasn't a valid password."
				elif not mismatch_passwords:
					error_mismatch_passwords = "Your passwords didn't match."

				if (not valid_email) and email != '':
					error_email = "That's not a valid email."

			self.write_form(error_username, error_password, 
				error_mismatch_passwords, error_email, username, email)

		else:
			self.redirect('/welcome?username=' + username)


class WelcomePage(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('username')

		if validate_username(username):
			self.response.out.write("Welcome, " + str(username) + "!")
		else:
			self.redirect('/')


app = webapp2.WSGIApplication([('/', MainPage),
								('/welcome', WelcomePage)],
								debug=True)