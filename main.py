#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import webapp2
import lxml.html
import lxml.etree
from google.appengine.api import urlfetch


MAIN_PAGE_HTML = """
<html>
  	<body>
    	<form action="/scraped" method="post">
      		<div><textarea name="content" rows="3" cols="60"></textarea></div>
      		<div><input type="submit" value="Scrape Website"></div>
    	</form>
  	</body>
</html>
"""

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write(MAIN_PAGE_HTML)

class Item(ndb.Model):
	title = ndb.StringProperty()
	img = ndb.LinkProperty()
	time_stamp = ndb.DateTimeProperty(auto_new_add=True)

class URL(ndb.Model):
	company = ndb.ReferenceProperty()
	url = ndb.LinkProperty()
	time_stamp = ndb.DateTimeProperty(auto_new_add=True)

class Company(ndb.Model):
	company = ndb.StringProperty()
	last_scrape = ndb.DateTimeProperty()
	time_stamp = ndb.DateTimeProperty(auto_new_add=True)

class Scraper(webapp2.RequestHandler):
    def post(self):
    	url = urlfetch.fetch(self.request.get('content'))
        doc = lxml.html.fromstring(url.content)

        for tag in doc.cssselect('title'):
			self.response.write(tag.text.encode('utf-8'))
			self.response.write('<br />')

        for img in doc.cssselect('link'):
        	if img.get('rel') == 'image_src':
				self.response.write('<img src="')
				self.response.write(img.get('href'))
				self.response.write('"><br />')

       	for price in doc.cssselect('div'):
       		if price.get('class') == 'sale-price':
				for savings in price.cssselect('strong'):
					self.response.write(savings.text.encode('utf-8'))
					self.response.write('<br />')
       		if price.get('class') == 'reg-price':
				self.response.write(price.text.encode('utf-8'))
				self.response.write('<br />')	
				for savings in price.cssselect('strong'):
					self.response.write(savings.text.encode('utf-8'))
					self.response.write('<br />')
	
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/scraped', Scraper),
], debug=True)
