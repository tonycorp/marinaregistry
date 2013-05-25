from google.appengine.ext import ndb

class Website(ndb.Model):
	name = ndb.StringProperty()

class Item(ndb.Model):
	title = ndb.StringProperty()
	img = ndb.StringProperty()
	price = ndb.StringProperty()
	sale = ndb.StringProperty()

class URL(ndb.Model):
	item = ndb.KeyProperty()
	url = ndb.StringProperty()
	last_scrape = ndb.DateTimeProperty()