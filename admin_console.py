import os
import jinja2
import webapp2
import urllib2
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])

class Admin(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()

		template_values = {'user' : user,}

		template = JINJA_ENVIRONMENT.get_template('header.html')
		self.response.write(template.render()) 	
		template = JINJA_ENVIRONMENT.get_template('admin.html')
		self.response.write(template.render(template_values))
		template = JINJA_ENVIRONMENT.get_template('footer.html')
		self.response.write(template.render())

class Admin2(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()

		template_values = {'user' : user,}

		template = JINJA_ENVIRONMENT.get_template('admin_console.html')
		self.response.write(template.render(template_values))