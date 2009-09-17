import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import model

import logging
log = logging.getLogger("simple")

class Charts(webapp.RequestHandler):
    def __init__(self):
        self.maxEnergy = 0

    def getAvgHR(self):
        query = model.Run.all()
        query.order('date')
        tmpResults = query.fetch(50)
        tmpResults1 = []
        for item in tmpResults:
            if item.hr:
                item.hr -= 100
                tmpResults1.append(item.hr)
        results = str(tmpResults1)
        results = results.replace(' ', '')
        results = results.replace('L', '')
        results = results.strip('[]')
        log.info(results)
        return results
    
    def getEnergy(self):
        query = model.Run.all()
        query.order('date')
        tmpResults = query.fetch(50)
        tmpResults1 = []
        for item in tmpResults:
            if item.energy:
                if item.energy > self.maxEnergy: self.maxEnergy=item.energy
                tmpResults1.append(item.energy)
        results = str(tmpResults1)
        results = results.replace(' ', '')
        results = results.replace('L', '')
        results = results.strip('[]')
        log.info(results)
        return results
    
    def get(self):
        self.user = users.get_current_user()
        if self.user:
            self.__render()
        else:
            self.redirect(users.create_login_url(self.request.uri))
           
    def __render(self):
        context = {'user': self.user.nickname(),
                       'logout_url': users.create_logout_url(self.request.uri),
                       'logout_txt': 'Logout',     
                       'results' : self.getAvgHR(),
                       'energy' : self.getEnergy(),
                       'max_energy' : self.maxEnergy
                   }
        path = os.path.join(os.path.dirname(__file__), 'templates/charts.html')
        self.response.out.write(template.render(path,context))

            
            