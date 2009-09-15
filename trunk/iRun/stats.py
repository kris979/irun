import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import model

import logging
log = logging.getLogger("simple")

class Stats(webapp.RequestHandler):
    def __init__(self):
        self.results = None
    
    def getLongestRuns(self):
        query = model.Run.all()
        query.order('-distance')
        self.results = query.fetch(5)
        
        

    def get(self):
        self.getLongestRuns()
        self.__render()
           
    def __render(self):
        user = users.get_current_user()
        if user:
#            runs = self.__getUserRuns(user)
            context = {'user': user.nickname(),
#                       'user_runs': runs,
                       'logout_url': users.create_logout_url(self.request.uri),
                       'logout_txt': 'Logout', 
                       'five_best':self.results
                       }
            path = os.path.join(os.path.dirname(__file__), 'templates/stats.html')
            self.response.out.write(template.render(path,context))
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
#    def __getUserRuns(self,user):
#        runs = []
#        user_runs = db.GqlQuery("SELECT * FROM Run WHERE author = :1 ORDER BY date DESC",user)
#        for run in user_runs:    
##            log.info('key:%s' %str(run.key()))
#            entry = {'date':run.date,'distance':run.distance,'duration':run.duration,'pace':run.pace,
#                    'pace_max':run.pace_max,'hr':run.hr,'hr_max':run.hr_max,'energy':run.energy,
#                    'te':run.te,'activity':run.activity,'key':str(run.key())}
#            runs.append(entry)
#        return runs
            
            
            