import webapp2
from google.appengine.api import mail
from google.appengine.api import users

class SendMail(webapp2.RequestHandler):

	def post(self):
		name = self.request.get('name')
		body = self.request.get('message')

		if name and body:
			message = mail.EmailMessage()
			message.sender = 'Tarantini Zirianov <tarantinizirianov@gmail.com>'
			message.to = 'Tarantini Zirianov <tarantinizirianov@gmail.com>'
			message.subject = 'New message from: ' + name
			message.body = body
			message.send()
			self.response.out.write('The lovers have been notified')
		elif name and  not body:
			self.response.out.write('C\'mon ' + name + ', I know you got something to say')
		elif body and not name:
			self.response.out.write('Sorry, but the owners don\'t like anonymity')
		else:
			self.response.out.write('Seriously, are you even trying? Do you not know how email works?')
