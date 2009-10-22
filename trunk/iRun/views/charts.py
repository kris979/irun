import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from data import data

import logging
log = logging.getLogger("simple")

class Charts(webapp.RequestHandler):
    def __init__(self):
        self.data = data.Data()
    
    def get(self):
        self.user = users.get_current_user()
        if self.user:
            self.__render()
        else:
            self.redirect(users.create_login_url(self.request.uri))
           
    def __render(self):
        energyData,maxEnergy = self.data.getEnergy()
        context = {'user': self.user.nickname(),
                       'logout_url': users.create_logout_url(self.request.uri),
                       'logout_txt': 'Logout',     
                       'results' : self.data.getAvgHR(),
                       'energy' : energyData,
                       'max_energy' : maxEnergy
                   }
        path = os.path.join(os.path.dirname(__file__), '../templates/charts.html')
        self.response.out.write(template.render(path,context))

            
            