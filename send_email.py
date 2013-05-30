import webapp2
from google.appengine.api import mail
from google.appengine.api import users

class SendMail(webapp2.RequestHandler):

	def post(self):
		user = users.get_current_user()
		if user is None:
			login_url = users.create_login_url(self.request.path)
			self.redirect(login_url)
			return

		message = mail.EmailMessage()
		message.sender = user.email()
		message.to = 'Tarantini Zirianov <tarantinizirianov@gmail.com>'
		message.subject = self.request.get('subject')
		message.body = self.request.get('message')
		message.send()