'''
Created on Sep 9, 2009

@author: kris
'''
from google.appengine.api import users
from google.appengine.ext import webapp
import model

class Err(webapp.RequestHandler):
    def post(self):
        self.response.out.write('<html><body>')
        self.response.out.write("error post")
        self.response.out.write('</body></html>')
    
    def get(self):
        self.response.out.write('<html><body>')
        self.response.out.write("error get")
        self.response.out.write('</body></html>')
        
        
        
        
#        
#              <form action="/" method="POST">
#      <div>
#      Date:<input type="text" name="Date" size="10">
#      Duration:<input type="text" name="Duration" size="5">
#      Distance:<input type="text" name="Distance" size="5">
#      Pace:<input type="text" name="Pace" size="5">
#      Pace max:<input type="text" name="Pace_max" size="5">
#      HR:<input type="text" name="HR" size="5">
#      HR max:<input type="text" name="HR_max" size="5">
#      Energy:<input type="text" name="Energy" size="5">
#      TE:<input type="text" name="TE" size="5">                                        
#      <input type="submit" value="Add">
#      </div>
#    </form>