'''
Created on Feb 23, 2014

@author: anamei92

'''

import maya.cmds as cmds
from pymel import *


    
def laplacianSmoothing():
    currObj = PyNode("pCube1");
    vtxList = currObj.vtx;
    print "hi"

'''
from pymel import *                   # safe to import into main namespace
for x in ls( type='transform'):
    print x.longName()                # object oriented design

    # make and break some connections
    x.sx >> x.sy                      # connection operator
    x.sx >> x.sz
    x.sx // x.sy                      # disconnection operator
    x.sx.disconnect()                 # smarter methods -- (automatically disconnects all inputs and outputs when no arg is passed)

    # add and set a string array attribute with the history of this transform's shape
    x.setAttr( 'newAt', x.getShape().history(), force=1 )

    # get and set some attributes
    x.rotate.set( [1,1,1] )
    trans = x.translate.get()
    trans *= x.scale.get()           # vector math
    x.translate.set( trans )         # ability to pass list/vector args
    mel.myMelScript(x.type(), trans) # automatic handling of mel procedures
    '''
laplacianSmoothing();