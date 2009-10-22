import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import data.model
import data.data

import logging
log = logging.getLogger()

class Stats(webapp.RequestHandler):
    def __init__(self):
        self.data = data.data.Data()
        self.templatePath = os.path.join(os.path.dirname(__file__), '../templates/stats.html')
        self.orderBy = 'date'
    
    def get(self):
        sortby = self.request.get('sort')
        if sortby:
            self.orderBy = sortby   
        if users.get_current_user():
            self.__render()
        else:
            self.redirect(users.create_login_url(self.request.uri))      
    
    def __render(self):
        context = {'user': users.get_current_user(),
                       'logout_url': users.create_login_url(self.request.uri),
                       'logout_txt': 'Logout', 
                       'headers' : data.model.headers,
                       'user_runs' : self.data.getUserRuns(self.orderBy)
                  }
        self.response.out.write(template.render(self.templatePath,context))