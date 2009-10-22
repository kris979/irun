import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from datetime import date
from datetime import timedelta
from data import model
from data import data

import logging
log = logging.getLogger()

class MainPage(webapp.RequestHandler):
    def __init__(self):
        self.form = model.RunForm()
        self.data = data.Data()
        self.templatePath = os.path.join(os.path.dirname(__file__), '../templates/index.html')

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
    
    def __render(self):
        context = {'user': users.get_current_user(),
                       'logout_url': users.create_login_url(self.request.uri),
                       'logout_txt': 'Logout', 
                       'form' : self.form,
                       'max_hart_rate' : self.data.getMaxHartRate(),
                       'max_pace' : self.data.getFastestPace(),
                       'longest_run' : self.data.getLongestRun(),
                       'fastest_5k' : self.data.getFastest(5),
                       'fastest_10k' : self.data.getFastest(10),
                       'fastest_15k' : self.data.getFastest(15),
                       'fastest_20k' : self.data.getFastest(20),
                  }
        self.response.out.write(template.render(self.templatePath,context))
    