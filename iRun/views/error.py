'''
Created on Sep 9, 2009

@author: kris
'''
from google.appengine.api import users
from google.appengine.ext import webapp
from data import model

class Err(webapp.RequestHandler):
    def post(self):
        self.response.out.write('<html><body>')
        self.response.out.write("error post")
        self.response.out.write('</body></html>')
    
    def get(self):
        self.response.out.write('<html><body>')
        self.response.out.write("error get")
        self.response.out.write('</body></html>')
