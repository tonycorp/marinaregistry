import os
import jinja2
import webapp2
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])

class FrontPage(webapp2.RequestHandler):
	def get(self):
		template_values = {
			'user' : users.get_current_user(),
			'login' : users.create_login_url('/'),
			'logout' : users.create_logout_url('/'),} 	
		template = JINJA_ENVIRONMENT.get_template('templates/main_page.html')
		self.response.write(template.render(template_values))