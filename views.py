import cgi
import webapp2
import lxml.html
import lxml.etree
from datetime import datetime
import webapp2
import urllib
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from models import Website, Item, URL

MAIN_PAGE_HTML_TOP = """
<html>
	<body>
		<form action="/scraper" method="post">
			<div>
			<select name="website">"""

MAIN_PAGE_HTML_BOTTOM = """
			</div>
      		<div><textarea name="content" rows="3" cols="60"></textarea></div>
      		<div><input type="submit" value="Add Item"></div>
      	</form>
    </body>
</html>"""

LISTINGS_HTML_TOP ="""
<!DOCTYPE HTML>
<html lang = "en">
	<head>
    	<meta charset = "UTF-8" />
    	<style type = "text/css">
    		table, td, th {
      			border: 1px solid black;
    		} 
    	</style>
  	</head>
	<body>
		<table>
			<tr>
				<th>Image</th>
				<th>Item</th>
				<th>Price</th>
				<th>On Sale</th>
			</tr>"""

LISTINGS_ROW = """
			<tr>
				<td>%s</td>
				<td>%s</td>
				<td>%s</td>
				<td>%s</td>
			</tr>"""

LISTING_HTML_BOTTOM = """
		</table>
	</body>
</html>"""

def website_key(website_name):
	return ndb.Key('Website', website_name)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write(MAIN_PAGE_HTML_TOP)
		websites = Website.query()
		for website in websites:
			self.response.write('			<option value="%s">%s</option>' % (website.name, website.name))
		self.response.write(MAIN_PAGE_HTML_BOTTOM)

class Scraper(webapp2.RequestHandler):
    def post(self):
    	registry_item = Item(parent=website_key(self.request.get('website')))
    	url = urlfetch.fetch(self.request.get('content'))
        doc = lxml.html.fromstring(url.content)

        for tag in doc.cssselect('title'):
			registry_item.title = tag.text.encode('utf-8')

        for img in doc.cssselect('link'):
        	if img.get('rel') == 'image_src':
				registry_item.img = img.get('href')

       	for price in doc.cssselect('div'):
       		if price.get('class') == 'sale-price':
				for savings in price.cssselect('strong'):
					registry_item.sale = savings.text.encode('utf-8')
       		if price.get('class') == 'reg-price':
				registry_item.price = price.text.encode('utf-8').replace("Reg.", "")
		registry_item.put()
		self.redirect('/listings')

class Listings(webapp2.RequestHandler):
	def get(self):
		self.response.write(LISTINGS_HTML_TOP)
		registry_items = Item.query()
		for item in registry_items:
			image = '<img src="%s"' % item.img
			price = item.price
			on_sale = 'No'
			if item.sale is not None:
				price = item.sale
				on_sale = 'Yes'
			self.response.write(LISTINGS_ROW % (image, item.title, price, on_sale))
		self.response.write(LISTING_HTML_BOTTOM)