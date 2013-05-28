import webapp2
from google.appengine.api import users

ADMIN_HTML = """
	<body>
		<form action="/scraper" method="post">
			<div>
			<select name="website">
				<option value="Canadian Tire">Canadian Tire</option>
			</select>
			</div>
      		<div><textarea name="content" rows="3" cols="60"></textarea></div>
      		<div><input type="submit" value="Add Item"></div>
      	</form>
    </body>
</html>"""

class Admin(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			greeting = ('Welcome, %s! (<a href="%s">Sign Out</a>)' % (user.nickname(), users.create_logout_url('/')))
		else:
			greeting = ('<a href=\"%s\">Sign in or register</a>' % users.create_login_url('/'))

		self.response.write('<html><head><p>%s</p></head>' % greeting)
		self.response.write(ADMIN_HTML)