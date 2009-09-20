import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import model

import logging
log = logging.getLogger()

class Stats(webapp.RequestHandler):
    def __init__(self):
        self.templatePath = os.path.join(os.path.dirname(__file__), 'templates/stats.html')
        self.orderBy = 'date'
    
    def __getUserRuns(self):
        query = model.Run.all()
        query.filter('author =', users.get_current_user()).order('-%s' %self.orderBy)
        user_runs = query.fetch(1000)
        return user_runs
           
    def __render(self):
        context = {'user': users.get_current_user(),
                       'logout_url': users.create_login_url(self.request.uri),
                       'logout_txt': 'Logout', 
                       'headers' : model.headers,
                       'user_runs' : self.__getUserRuns()
                  }
        self.response.out.write(template.render(self.templatePath,context))
    
    def get(self):
        sortby = self.request.get('sort')
        if sortby:
            self.orderBy = sortby   
        if users.get_current_user():
            self.__render()
        else:
            self.redirect(users.create_login_url(self.request.uri))      