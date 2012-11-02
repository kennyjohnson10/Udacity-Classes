import webapp2

form = '''
		<header>The Form</header>
		<form method="post">
			What is your birthday?
			<br>
			<label>
				month
				<input type="text" name="month">
			</label>
			<label>
				day
				<input type="text" name="day">
			</label>
			<label>
				year
				<input type="text" name="year">
			</label>

			<br>
			<br>
			<input type="submit">
		</form>
		'''

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write(form)

	def post(self):
		self.response.out.write("Thanks! That's a totally valid day.")


app = webapp2.WSGIApplication([('/', MainPage)],
								debug=True)