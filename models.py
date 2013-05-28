from google.appengine.ext import ndb

class Item(ndb.Model):
	title = ndb.StringProperty()
	img = ndb.StringProperty()
	price = ndb.StringProperty()
	sale = ndb.StringProperty()

class URL(ndb.Model):
	url = ndb.StringProperty()
	last_scrape = ndb.DateTimeProperty()