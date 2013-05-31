import cgi
import webapp2
import lxml.html
import lxml.etree
import datetime
import json
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from models import Item, URL

class ScrapePage(webapp2.RequestHandler):
  def post(self):
    url = urlfetch.fetch(self.request.get('url'))
    doc = lxml.html.fromstring(url.content)

    my_response = {};

    for sku in doc.cssselect('span'):
      if sku.get('id') == 'displaySkuCode':
        my_response['sku'] = sku.text

    for tag in doc.cssselect('title'):
      my_response['title'] = tag.text.encode('utf-8').replace(' | Canadian Tire', '')

    for img in doc.cssselect('link'):
      if img.get('rel') == 'image_src':
        my_response['img'] = img.get('href')

    for price in doc.cssselect('div'):
      if price.get('class') == 'sale-price':
        for savings in price.cssselect('strong'):
          my_response['sale'] = savings.text.encode('utf-8')
      else:
        my_response['sale'] = ''
      if price.get('class') == 'reg-price':
        my_response['price'] = price.text.encode('utf-8').replace("Reg.", "")

    my_response['url'] = self.request.get('url')

    self.response.out.write(json.dumps(my_response))