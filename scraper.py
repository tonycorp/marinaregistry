import cgi
import webapp2
import lxml.html
import lxml.etree
import urllib
import datetime
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from models import Item, URL

class Scraper(webapp2.RequestHandler):
  def post(self):
    url = urlfetch.fetch(self.request.get('content'))
    doc = lxml.html.fromstring(url.content)

    for sku in doc.cssselect('span'):
      if sku.get('id') == 'displaySkuCode':
        item_id = sku.text

    registry_item = Item.get_by_id(item_id)
    if registry_item is None:
      registry_item = Item(id=item_id, parent=ndb.Key("Website", self.request.get('website')))

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
    
    registry_item.category = self.request.get('category')
    registry_item.for_who = self.request.get('for_who')
    registry_item.put()

    link = URL.get_by_id(item_id)
    if link is None:
      link = URL(id=item_id, parent=ndb.Key("Website", self.request.get('website')))
    link.url = self.request.get('content')
    link.last_scrape = datetime.datetime.now()
    link.put()

    self.redirect('/listings')