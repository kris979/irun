'''
Created on Sep 10, 2009

@author: kris
'''
import datetime
from google.appengine.tools import bulkloader
from data import model

class RunLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Run',
                               [
#                                ('author', str),
#                                ('added',lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date()),
                                ('date',lambda x: datetime.datetime.strptime(x, '%d/%m/%Y').date()),
                                ('duration',lambda x: datetime.datetime.strptime(x, '%H:%M:%S').time()),
                                ('distance', float),
                                ('pace',lambda x: datetime.datetime.strptime(x, '%H:%M:%S').time()),
                                ('pace_max',lambda x: datetime.datetime.strptime(x, '%H:%M:%S').time()),
                                ('hr', int),
                                ('hrmax', int),
                                ('energy', int),
                                ('te', float),     
                               ])

loaders = [RunLoader]