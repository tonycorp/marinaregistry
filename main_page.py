import os
import jinja2
import webapp2
from datetime import date
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])

class FrontPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		month_list = [31,28,31,30,31,30,31,31,30,31,30,31]
		delta = date(2014, 8, 12) - date.today()
		time_in_days = delta.days
		i = date.today().month - 1
		years = 0
		months = 0
		days = 0
		while time_in_days > 0:
			if time_in_days >= month_list[i]:
				months += 1
				time_in_days -= month_list[i]
			else:
				days = time_in_days
				time_in_days = 0
			if months > 11:
				years += 1
				months = 0
			i += 1
			if i > 11:
				i = 0

		weeks = days/7
		days = days%7

		if years > 1:
			years = str(years) + ' years, '
		elif years == 1:
			years = str(years) + ' year, '
		else:
			years = ''

		if months > 1:
			months = str(months) + ' months, '
		elif months == 1:
			months = str(months) + ' month, '
		else:
			months = ''

		if weeks > 1:
			weeks = str(weeks) + ' weeks, '
		elif weeks == 1:
			weeks = str(weeks) + ' week, '
		else:
			weeks = ''

		if days > 1:
			days = 'and ' + str(days) + ' days'
		elif days == 1:
			days = 'Tomorrow'
		else:
			years = 'Today'

		template_values = {
			'user' : user,
			'years' : years,
			'months' : months,
			'weeks' : weeks,
			'days' : days,
			'user_is_admin' : 'Yes' if users.is_current_user_admin() else 'No',}

		template = JINJA_ENVIRONMENT.get_template('header.html')
		self.response.write(template.render()) 	
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))
		template = JINJA_ENVIRONMENT.get_template('footer.html')
		self.response.write(template.render())