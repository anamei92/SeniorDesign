'''
Created on Feb 26, 2014

@author: anamei92
'''
import nameUtils, xformUtils

def reloadIt():
    reload(nameUtils)
    reload(xformUtils)
    
    print "------------>UTILS RELOAD: OK"