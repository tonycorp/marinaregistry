import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
from models import Item

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
				<th>Website</th>
			</tr>"""

LISTINGS_ROW = """
			<tr>
				<td>%s</td>
				<td>%s</td>
				<td>%s</td>
				<td>%s</td>
				<td>%s</td>
			</tr>"""

LISTING_HTML_BOTTOM = """
		</table>
	</body>
</html>"""

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
			self.response.write(LISTINGS_ROW % (image, item.title, price, on_sale, item.key.parent().string_id()))
		self.response.write(LISTING_HTML_BOTTOM)