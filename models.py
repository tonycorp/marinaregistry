from google.appengine.ext import ndb

class Item(ndb.Model):
	title = ndb.StringProperty()
	img = ndb.StringProperty()
	price = ndb.StringProperty()
	sale = ndb.StringProperty()
	category = ndb.StringProperty()
	for_who = ndb.StringProperty()
	status = ndb.StringProperty()
	gifter = ndb.UserProperty()

class URL(ndb.Model):
	url = ndb.StringProperty()
	last_scrape = ndb.DateTimeProperty()
