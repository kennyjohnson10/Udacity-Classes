import webapp2
import cgi
import string

form = '''
<!DOCTYPE html>
<html>
<head>
<title>My ROT13 Site</title>
</head>
<body>
<h2>Enter some text to ROT13:</h2>
<form method="post">
<br>
<textarea type="text" style="width:400px;height:100px;" name="text">
%(input_text)s
</textarea>

<br>
<input type="submit">
</form>
</body>
</html>
		'''

lowercase_alpha = string.ascii_lowercase
uppercase_alpha = string.ascii_uppercase
len_lowercase_alpha = len(lowercase_alpha)
len_uppercase_alpha = len(uppercase_alpha)


def escape_html(s):
	return cgi.escape(s, quote = True)


class MainPage(webapp2.RequestHandler):
	# ROT13 encyption algorithm
	def rot13(self, s):
		new_s = ''

		for char in s:
			if char in lowercase_alpha:
				new_s += lowercase_alpha[(lowercase_alpha.find(char) + 13) % len_lowercase_alpha]
			elif char in uppercase_alpha:
				new_s += uppercase_alpha[(uppercase_alpha.find(char) + 13) % len_uppercase_alpha]
			else:
				new_s += char
		
		return new_s

	def write_form(self, input_text=""):
		self.response.out.write(form % {'input_text': escape_html(input_text)})

	def get(self):
		self.write_form()

	def post(self):
		text_data = self.request.get('text')
		text_data = self.rot13(text_data)
		self.write_form(text_data)


app = webapp2.WSGIApplication([('/', MainPage)],
								debug=True)