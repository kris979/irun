import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from datetime import date
import model

import logging
log = logging.getLogger()

class MainPage(webapp.RequestHandler):
    def __init__(self):
        self.form = model.RunForm()
        self.templatePath = os.path.join(os.path.dirname(__file__), 'templates/index.html')

    def get(self):
        if users.get_current_user():
            self.__render()
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
    def post(self):
        data = model.RunForm(data=self.request.POST)
        if data.is_valid():
            run = data.save(commit=False) #get data from the form
            if users.get_current_user():
                run.author = users.get_current_user()
            run.added = date.today()
            run.put()
            self.redirect(self.request.uri)
        else:
            self.form = data
            self.__render()
        
    def __getUserRuns(self):
        query = model.Run.all()
        query.filter('author =', users.get_current_user()).order('-%s' %self.orderBy)
        user_runs = query.fetch(1000)
        return user_runs
    
    def __render(self):
        context = {'user': users.get_current_user(),
                       'logout_url': users.create_login_url(self.request.uri),
                       'logout_txt': 'Logout', 
                       'form' : self.form,
                       'max_hart_rate' : self.getMaxHartRate(),
                       'max_pace' : self.getFastestPace(),
                       'longest_run' : self.getLongestRun(),
                       'fastest_5k' : self.getFastest(5.0),
                       'fastest_10k' : self.getFastest(10.0),
                       'fastest_15k' : self.getFastest(15.0),
                       'fastest_20k' : self.getFastest(20.0),
                  }
        self.response.out.write(template.render(self.templatePath,context))
    
    def getLongestRun(self):
        q = model.Run.all()
        q.filter('author =', users.get_current_user())
        q.order('-distance')
        results = q.fetch(1)
        if len(results) > 0:
            return results[0]
        else:
            return None
        
    def getMaxHartRate(self):
        q = model.Run.all()
        q.filter('author =', users.get_current_user())
        q.order('-hr_max')
        results = q.fetch(1)
        if len(results) > 0:
            return results[0]
        else:
            return None
    
    def getFastest(self, distance):
        q = model.Run.all()
        q.filter('author =', users.get_current_user())
        q.filter('activity =','run')
        q.filter('distance >=',distance)
        results = q.fetch(1000)
        if len(results) == 0:
            return None
        best = results[0].duration
        for result in results:
            if result.duration < best:
                best = result.duration 
        return best  
        
    def getFastestPace(self):
        q = model.Run.all()
        q.filter('author =', users.get_current_user())
        q.filter('activity =','run')
        q.order('pace_max')
        results = q.fetch(1)
        if len(results) > 0:
            return results[0]
        else:
            return None       