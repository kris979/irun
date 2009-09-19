'''
Created on Sep 12, 2009

@author: kris
'''
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.api import mail
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

    def prepareExportCSVFile(self):
        csv = ''
        for k in model.headers.keys():
            csv += k
            csv += ','
        csv = csv.rstrip(',')
        csv += '\n'
        q = model.Run.all()
        q.filter('author =', users.get_current_user())
        q.order('-date')
        results = q.fetch(1000)
        for run in results:
            line = str(run.date) + ',' + str(run.duration) + ',' + str(run.distance) + ',' + str(run.hr) \
             + ',' + str(run.hr_max) + ',' + str(run.pace) + ',' + str(run.pace_max) + ',' + str(run.te) + ',' \
             + str(run.energy) + ',' + run.activity + '\n'
            csv += line
        return csv
         
    def sendEmail(self):
        to_addr = users.get_current_user().email()
        if not mail.is_email_valid(to_addr):
            # Return an error message...
            pass
        message = mail.EmailMessage(attachments=[('workout.csv',self.prepareExportCSVFile())])
        message.sender = users.get_current_user().email()
        message.to = to_addr
        message.subject = 'chartmyrun.appspot.com sending workout.csv'
        message.body = """Your workout file has been successfully exported""" 
        message.send()
        self.redirect('/')

    def prepareDataForSaving(self,content):
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

    def addInstanceToDb(self,row):
        run = model.Run()
        if users.get_current_user():
            run.author = users.get_current_user()
        run.added = datetime.date.today()
        run.date = d(row[0])
        run.duration = duration(row[1])
        run.distance = float(row[2])
        run.hr = int(row[3])
        run.hr_max = int(row[4])
        run.pace = pace(row[5])
        run.pace_max = pace(row[6])
        run.te = float(row[7])
        run.energy = int(row[8])
        run.activity = row[9]
        run.put()
        
    def save(self,content):
        self.prepareDataForSaving(content)
        for row in self.rows:
            self.addInstanceToDb(row)
        
    def post(self):
        content = self.request.get('csv')
        if content:
            self.save(content)
            self.redirect('/')
        else:
            log.error('error uploading csv file')
#            self.redirect('/error')
            self.response.out.write('<html><body>')
            self.response.out.write("<p>error when uploading a file</p>")
            self.response.out.write('</body></html>')
            
    def get(self):
        self.sendEmail()
#        self.redirect('/err')
    