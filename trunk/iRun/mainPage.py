import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from datetime import date
import model

#import logging
#log = logging.getLogger()

class MainPage(webapp.RequestHandler):
    def __init__(self):
        self.user = users.get_current_user()
        self.form = model.RunForm()
        self.templatePath = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.orderBy = 'date'
        self.context = {'user': self.user.nickname(),
                        'logout_txt': 'Logout'}

    def get(self):
        sortby = self.request.get('sort')
        if sortby:
            self.orderBy = sortby   
        self.__render()
            
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
        query = "SELECT * FROM Run WHERE author = :1 ORDER BY %s DESC" %self.orderBy
        user_runs = db.GqlQuery(query,self.user)
        return user_runs
    
    def __render(self):
        if self.user:
            self.context['user_runs'] =  self.__getUserRuns()    
            self.context['form'] = self.form
            self.context['logout_url'] = users.create_logout_url(self.request.uri),
            self.response.out.write(template.render(self.templatePath,self.context))
        else:
            self.redirect(users.create_login_url(self.request.uri))
        
#    def setForm(self,aform):
#        self.form = aform
#    setform = staticmethod(setForm)
            
            
            