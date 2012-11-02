import webapp2
import cgi

form = '''
		<header>The Form</header>
		<form method="post">
			What is your birthday?
			<br>
			<label>
				month
				<input type="text" value="%(month)s" name="month">
			</label>
			<label>
				day
				<input type="text" value="%(day)s" name="day">
			</label>
			<label>
				year
				<input type="text" value="%(year)s" name="year">
			</label>
			<div style="color:red">%(error)s</div>

			<br>
			<br>
			<input type="submit">
		</form>
		'''

months = ['January',

		  'February',

		  'March',

		  'April',

		  'May',

		  'June',

		  'July',

		  'August',

		  'September',

		  'October',

		  'November',

		  'December'] 


# The valid_day() function takes as input a String, and returns either a valid 
# Int or None. If the passed in String is not a valid day, return None. 
# If it is a valid day, then return the day as an Int, not a String. Don't 
# worry about months of different length. Assume a day is valid if it is a number 
# between 1 and 31.

def valid_day(day):
	if day and day.isdigit():
		day = int(day)
		if day <= 31 and day > 0:
			return day

# If the passed in parameter 'month' is not a valid month, return None. 
# If 'month' is a valid month, then return the name of the month with the first letter
# capitalized.

month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_month(month):
	if month:
		short_month = month[:3].lower()
		return month_abbvs.get(short_month)

# Function for character escapsing.
def escape_html1(s):
	for (i, o) in (('&', '&amp'),
				('<', '&lt'),
				('>', '&gt'),
				('"', '&quot')):
		s.replace(i, o)
	return s

def escape_html(s):
	return cgi.escape(s, quote = True)

# If the passed in parameter 'year' is not a valid year, return None. If 'year'
# is a valid year, then return the year as a number. Assume a year is valid
# if it is a number between 1900 and 2020.

def valid_year(year):
	if year.isdigit():
		year = int(year)
		if year >= 1900 and year <= 2020:
			return year


class MainPage(webapp2.RequestHandler):
	def write_form(self, error="", month="", day="", year=""):
		self.response.out.write(form % {'error': escape_html(error), 
										'month': escape_html(month), 
										'day': escape_html(day), 
										'year': escape_html(year)
										})

	def get(self):
		self.write_form()

	def post(self):
		user_day = self.request.get('day')
		user_month = self.request.get('month')
		user_year = self.request.get('year')

		day = valid_day(user_day)
		month = valid_month(user_month)
		year = valid_year(user_year)

		if not (day and month and year):
			self.write_form("That doesn't look valid to me.", 
							user_month, 
							user_day, 
							user_year)
		else:
			self.redirect('/thanks')

class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Thanks! That's a totally valid day.")

app = webapp2.WSGIApplication([('/', MainPage)
								('/thanks', ThanksHandler)],
								debug=True)