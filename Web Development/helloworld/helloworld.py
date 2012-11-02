import webapp2

form = '''
		<header>HTTP form 1</header>
		<form action="/testform">
			<input name="q">
			<input type="submit">
		</form>

		<header>HTTP form 2</header>
		<form action="/HTTPtestform">
			<input name="q">
			<input type="submit">
		</form>

		<header>Post form</header>
		<form method="post" action="/postTestForm">
			<input name="q">
			<input type="submit">
		</form>
		<header>HTTP Post form</header>
		<form method="post" action="/HTTPpostTestForm">
			<input name="q">
			<input type="submit">
		</form>

		<header>password type form</header>
		<form>
			<input type="password" name="q">
			<input type="submit">
		</form>

		<header>checkbox form</header>
		<form>
			<input type="checkbox" name="q">
			<input type="checkbox" name="r">
			<input type="checkbox" name="s">
			<br>
			<input type="submit">
		</form>

		<header>radiobutton form</header>
		<form>
			<input type="radio" name="q" value="one">
			<input type="radio" name="q" value="two">
			<input type="radio" name="q" value="three">
			<br>
			<input type="submit">
		</form>

		<header>labeled radiobutton form</header>
		<form>
			<label>
				one
				<input type="radio" name="q" value="one">
			</label>

			<label>
				two
				<input type="radio" name="q" value="two">
			</label>

			<label>
				three
				<input type="radio" name="q" value="three">
			</label>
			<br>
			<input type="submit">
		</form>

		<header>dropdown form</header>
		<form>
			<select name="q">
				<option value="1">one</option>
				<option value="2">two</option>
				<option value="3">three</option>
			</select>

			<br>
			<input type="submit">
		</form>
		'''

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write(form)


class TestHandler(webapp2.RequestHandler):
	def get(self):
		q = self.request.get('q')
		self.response.out.write(q)


class HTTPTestHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write(self.request)

class PostTestHandler(webapp2.RequestHandler):
	def post(self):
		q = self.request.get('q')
		self.response.out.write(q)


class HTTPPostTestHandler(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write(self.request)


app = webapp2.WSGIApplication([('/', MainPage),
								('/testform', TestHandler),
								('/HTTPtestform', HTTPTestHandler),
								('/postTestForm', PostTestHandler),
								('/HTTPpostTestForm', HTTPPostTestHandler)],
								debug=True)