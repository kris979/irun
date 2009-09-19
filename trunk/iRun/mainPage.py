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
        self.orderBy = 'date'

    def get(self):
        sortby = self.request.get('sort')
        if sortby:
            self.orderBy = sortby   
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
        headers = []
        for v in model.headers.itervalues():
            headers.append(v)
        context = {'user': users.get_current_user(),
                       'logout_url': users.create_login_url(self.request.uri),
                       'logout_txt': 'Logout', 
                       'headers' : headers,
                       'user_runs' :  self.__getUserRuns(),    
                       'form' : self.form
                  }
        self.response.out.write(template.render(self.templatePath,context))
             
            