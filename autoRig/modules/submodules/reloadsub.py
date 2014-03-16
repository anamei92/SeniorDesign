'''
Created on Mar 11, 2014

@author: anamei92
'''

import boneChain
import control
import fkChain, ikChain

def reloadIt():
    reload(boneChain)
    reload(control)
    reload(fkChain)
    reload(ikChain)
    
    print "------------>SUBMODULES RELOAD: OK"