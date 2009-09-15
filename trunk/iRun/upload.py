'''
Created on Sep 12, 2009

@author: kris
'''
from google.appengine.ext import webapp
from google.appengine.api import users
import datetime
import model
import logging

log = logging.getLogger("simple")
d = lambda x: datetime.datetime.strptime(x, '%d/%m/%y').date()
duration = lambda x: datetime.datetime.strptime(x, '%H:%M:%S').time()
pace = lambda x: datetime.datetime.strptime(x, '%M:%S').time()

class AddCSV(webapp.RequestHandler):
    header = None
    rows = None

    def processContent(self,content):
        rows = content.split('\n')
        newRows = []
        for row in rows:
            elements = row.split(",")
            newElements = []
            for element in elements:
                newElements.append(element.strip('"'))
            newRows.append(newElements)
        self.header = newRows[0]
        self.rows = newRows[1:]

    def save(self):
        for row in self.rows:
            run = model.Run()
            if users.get_current_user():
                    run.author = users.get_current_user()
            run.added = datetime.date.today()
            run.date = d(row[0])
            run.duration = duration(row[1])
            run.distance = float(row[2])
            run.hr = int(row[3])
            run.hrmax = int(row[4])
            run.pace = pace(row[5])
            run.pace_max = pace(row[6])
            run.te = float(row[7])
            run.energy = int(row[8])
            run.activity = row[9]
            run.put()
        
    def post(self):
        content = self.request.get('csv')
        if content:
            self.processContent(content)
            self.save()
            self.redirect('/')
        else:
            self.response.out.write('<html><body>')
            self.response.out.write("<p>error when uploading a file</p>")
            self.response.out.write('</body></html>')
        
#    def put(self):
#        uploaded_file = self.request.body
#        self.response.out.write('<html><body>')
#        if uploaded_file:
#            self.response.out.write("<p>%s</p>" %uploaded_file)
#        else:
#            self.response.out.write("<p>empty put</p>")
#        self.response.out.write('</body></html>')