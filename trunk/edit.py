'''
Created on Sep 12, 2009
@author: kris
'''

from google.appengine.ext import webapp
from google.appengine.ext import db
import model

import logging

log = logging.getLogger("simple")

class Edit(webapp.RequestHandler):
    def get(self):
        id = self.request.get('id')
        item = model.Run.get(db.Key(id))
        db.delete(item)
        self.response.out.write('<html><body>'
                                '<form method="POST" '
                                'action="/">'
                                '<table>')
        self.response.out.write(model.RunForm(instance=item))
        self.response.out.write('</table>'
                                '<input type="hidden" name="_id" value="%s">'
                                '<input type="submit" value="Update">'
                                '</form></body></html>' % id)
        
class Delete(webapp.RequestHandler):
    def get(self):
        id = self.request.get('id')
        key = db.Key(id)
        item = model.Run.get(key)
        if item:
            db.delete(item)
        self.redirect('/')