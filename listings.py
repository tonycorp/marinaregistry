import os
import jinja2
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
from models import Item

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])

class Listings(webapp2.RequestHandler):
	def get(self):
		template_values = {'items' : Item.query(),} 	
		template = JINJA_ENVIRONMENT.get_template('templates/listings.html')
		self.response.write(template.render(template_values))