import webapp2
from google.appengine.api import users

class FrontPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			greeting = ('Welcome, %s! (<a href="%s">Sign Out</a>)' % (user.nickname(), users.create_logout_url('/')))
		else:
			greeting = ('<a href=\"%s\">Sign in or register</a>' % users.create_login_url('/'))

		self.response.write('<html><head><p>%s</p></head>' % greeting)
		self.response.write('<body><a href="./admin">Admin Console</a>')
		self.response.write('<a href="./listings">Listings</a></body></html>')