'''
Created on Sep 24, 2009

@author: kris
'''
import model
from google.appengine.api import users
from datetime import timedelta

import logging
log = logging.getLogger("simple")

class Data(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def getUserRuns(self,orderBy):
        query = model.Run.all()
        query.filter('author =', users.get_current_user()).order('-%s' %orderBy)
        user_runs = query.fetch(1000)
        return user_runs    
    
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
        q.filter('distance >=',float(distance))
        results = q.fetch(1000)
        if len(results) == 0:
            return None
        best = timedelta(hours=9)
        for result in results:
            k_pace = timedelta(hours=result.pace.hour,minutes=result.pace.minute,seconds=result.pace.second)
            timeForGivenDistance = k_pace*distance
            if timeForGivenDistance < best:
                best = timeForGivenDistance
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
    
    def getAvgHR(self):
        query = model.Run.all()
        query.filter('author =', users.get_current_user())
        query.order('date')
        tmpResults = query.fetch(50)
        tmpResults1 = []
        for item in tmpResults:
            if item.hr:
                item.hr -= 100
                tmpResults1.append(item.hr)
        results = str(tmpResults1)
        results = results.replace(' ', '')
        results = results.replace('L', '')
        results = results.strip('[]')
        log.info(results)
        return results
    
    def getEnergy(self):
        maxEnergy = 0
        query = model.Run.all()
        query.filter('author =', users.get_current_user())
        query.order('date')
        tmpResults = query.fetch(50)
        tmpResults1 = []
        for item in tmpResults:
            if item.energy:
                if item.energy > maxEnergy: maxEnergy=item.energy
                tmpResults1.append(item.energy)
        results = str(tmpResults1)
        results = results.replace(' ', '')
        results = results.replace('L', '')
        results = results.strip('[]')
        log.info(results)
        return results,maxEnergy