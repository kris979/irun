import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from datetime import date
import model

import logging
log = logging.getLogger("simple")

class MainPage(webapp.RequestHandler):
    def __init__(self):
        self.form = model.RunForm()
        self.orderBy = 'date'

    def get(self):
        sortby = self.request.get('sort')
#        log.info(sortby)
        if sortby:
            self.orderBy = sortby   
        self.__render()
            
    def post(self):
        data = model.RunForm(data=self.request.POST)
        if data.is_valid():
            # Save the data, and refresh
            run = data.save(commit=False)
            if users.get_current_user():
                run.author = users.get_current_user()
            run.added = date.today()
#            log.info("added: %s" %str(run.added))
#            log.info("date: %s" %str(run.date))
            run.put()
            self.redirect(self.request.uri)
        else:
            self.form = data
            self.__render()
            
    def setForm(self,aform):
        self.form = aform
    setform = staticmethod(setForm)
        
    def __getUserRuns(self,user):
        runs = []
        query = "SELECT * FROM Run WHERE author = :1 ORDER BY %s DESC" %self.orderBy
        log.info(query)
        user_runs = db.GqlQuery(query,user)
        for run in user_runs:    
#            log.info('key:%s' %str(run.key()))
            entry = {'date':run.date,'distance':run.distance,'duration':run.duration,'pace':run.pace,
                    'pace_max':run.pace_max,'hr':run.hr,'hr_max':run.hr_max,'energy':run.energy,
                    'te':run.te,'activity':run.activity,'key':str(run.key())}
            runs.append(entry)
        return runs
    
    def __render(self):
        user = users.get_current_user()
        if user:
            runs = self.__getUserRuns(user)
            context = {'user': user.nickname(),
                       'user_runs': runs,
                       'logout_url': users.create_logout_url(self.request.uri),
                       'logout_txt': 'Logout',     
                       'form' : self.form }
            path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
            self.response.out.write(template.render(path,context))
        else:
            self.redirect(users.create_login_url(self.request.uri))
        

            
            
            