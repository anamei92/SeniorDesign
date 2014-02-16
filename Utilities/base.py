'''
Created on Aug 6, 2013

@author: anamei92

This Module does not import any of our other modules from 
our package
'''
import maya.cmds as cmds
import functions

'''
Create group for an object. Zero out all
translation/rotation on the original object
add it to the top parent node.

numGroups = how many groups to create
default value = 2

'''
class Base(object):
    def __init__(self, name = None):
        if not name:
            name = cmds.ls(sl = 1)[0]
        self.name = name
        self.originalName = name
        
     #unique name functions    
    def unique_name(self):
        functions.unique_name(self.name)
   
'''
Base class group
includes duplicate and unique name
'''
class BaseDagNode (Base):
        
    #group and zero out objects 
    def group_object(self,numGroups = 2):
        self.groups = functions.group_object([self.name], numGroups = numGroups)
          
    #duplicate and mirror along an axis
    def duplicate(self, mirror_axis='x'):
        functions.duplicate(self.name, mirror_axis = mirror_axis)

#var = BaseDagNode()
#var.group_object(2)
#var.duplicate("x")