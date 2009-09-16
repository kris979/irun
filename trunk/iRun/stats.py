import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import model

import logging
log = logging.getLogger()

class Stats(webapp.RequestHandler):
    def __init__(self):
        self.user = users.get_current_user()
        self.templatePath = os.path.join(os.path.dirname(__file__), 'templates/stats.html')
    
    def getFiveLongestRuns(self):
        query = model.Run.all()
        query.filter('activity =','run').order('-distance')
        return query.fetch(5)
    
    def getMaxHartRate(self):
        q = model.Run.all()
#        q.filter('activity =','run')
        q.order('-hr_max')
        results = q.fetch(1)
#        for r in results:
#            log.info(r.hrmax)
        return results[0]
    
    def getFastestPace(self):
        q = model.Run.all()
        q.filter('activity =','run')
        q.order('pace_max')
        results = q.fetch(1)
        return results[0]
    
    def get(self):
        self.__render()
           
    def __render(self):
        context = {'user': self.user.nickname(),
                       'logout_url': users.create_logout_url(self.request.uri),
                       'logout_txt': 'Logout', 
                       'five_longest_runs':self.getFiveLongestRuns(),
                       'max_hart_rate' : self.getMaxHartRate(),
                       'max_pace' : self.getFastestPace()
                  }
        self.response.out.write(template.render(self.templatePath,context))
            