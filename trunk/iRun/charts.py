import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import model

import logging
log = logging.getLogger("simple")

class Charts(webapp.RequestHandler):
    def __init__(self):
        self.user = users.get_current_user()

    def getData(self):
        query = model.Run.all()
        query.order('date')
        tmpResults = query.fetch(20)
        results = []
        for item in tmpResults:
            if item.hr:
                log.info(item.hr)
                item.hr = int(item.hr) - 100
                results.append(item)
        return results
        
    def get(self):
        self.__render()
           
    def __render(self):
        context = {'user': self.user.nickname(),
                       'logout_url': users.create_logout_url(self.request.uri),
                       'logout_txt': 'Logout',     
                       'results' : self.getData() 
                   }
        path = os.path.join(os.path.dirname(__file__), 'templates/charts.html')
        self.response.out.write(template.render(path,context))

            
            