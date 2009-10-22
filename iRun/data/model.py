'''
Created on Sep 6, 2009
@author: kris
'''
from google.appengine.ext import db
from google.appengine.ext.webapp import template #must be here otherwise appEngine will complain about django settings file
from google.appengine.ext.db import djangoforms

headers = ['Date (dd/mm/yy)','Duration(hh:mm:ss)','Distance (km)','Pace(min/km)',
           'Pace max (min/km)','HR (bpm)','HR max (bpm)','Energy(kcal)','TE','Activity']

class Run(db.Model):
    author = db.UserProperty()
    added = db.DateProperty()
    date = db.DateProperty()
    duration = db.TimeProperty()
    distance = db.FloatProperty()
    pace = db.TimeProperty()
    pace_max = db.TimeProperty()
    hr = db.IntegerProperty()
    hr_max = db.IntegerProperty()
    energy = db.IntegerProperty()
    te = db.FloatProperty()
    activity = db.StringProperty()

#input_formats=['%d/%m/%Y']
class RunForm(djangoforms.ModelForm):
    date = djangoforms.forms.DateField(input_formats=['%d/%m/%y']) 
    class Meta:
        model = Run
        exclude = ['author','added']
        


