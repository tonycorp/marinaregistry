import os
import jinja2
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
from models import Item

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])

class BothList(webapp2.RequestHandler):
	def get(self):
		template_values = {'items' : Item.query(),
		'user_is_admin' : 'Yes' if users.is_current_user_admin() else 'No',}
		
		template = JINJA_ENVIRONMENT.get_template('header.html')
		self.response.write(template.render()) 	
		template = JINJA_ENVIRONMENT.get_template('listings.html')
		self.response.write(template.render(template_values))
		template = JINJA_ENVIRONMENT.get_template('footer.html')
		self.response.write(template.render())