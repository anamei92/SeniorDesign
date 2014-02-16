'''
Created on Jul 19, 2013

@author: anamei92
'''
import maya.cmds as cmds
#from Utilities import base
import base
'''
Create group for an object. Zero out all
translation/rotation on the original object
add it to the top parent node.

numGroups = how many groups to create
default value = 2

'''
def group_object(current_objects=None, numGroups = 2):
    
    if not current_objects:
        current_objects = cmds.ls(sl=True)[0]
    #get the transformation matrix of the input object
    my_matrix = cmds.xform(current_objects, query=1, matrix=1)
    #loop
    x = 0
    while x < numGroups:
        cmds.group()
        x = x+1
    
    group = cmds.ls(sl = True)[0]
    identity = cmds.xform(group, query=1, matrix=1)
    cmds.xform(current_objects, matrix=identity, worldSpace=1, absolute=1)
    cmds.xform(group, matrix=my_matrix, worldSpace=1, absolute=1)
    return group 
  
def unique_name(current_object):
    #select all objects
    maya_scene = cmds.ls()
    print current_object
    if "_" in current_object:
        name_list = list(current_object.partition("_"))
        name_list.insert(-2, "_{0:03}")
        print name_list
        new_name = ""
        
        for each_section in name_list:
            new_name += each_section
        
        #cmds.rename(current_object, new_name)
        
    else: 
        new_name = "{0}_{1}".format(current_object, "{0:03}") 
    print "new_name" , new_name         
    counter = 1 
    while current_object in maya_scene:
        current_object = new_name.format(counter)
        counter += 1
    
    return current_object

#print unique_name(cmds.ls(sl=1)[0])
  
def duplicate(current_object, mirror_axis='x'):
    
    if not current_objects:
        current_objects = cmds.ls(sl=True)[0]
    axis_list = "xyz"                
    my_matrix = cmds.xform(current_object, query=1, matrix=1)
    counter = 0
    axis_index = axis_list.index(mirror_axis)
    
    for each_index, each_value in enumerate(my_matrix[:11]):
        if axis_list.index(mirror_axis) != each_index - (4 * counter):
            my_matrix[each_index] = each_value * -1
        
        if not (each_index + 1) % 4:
            counter += 1
            
    my_matrix[12 + axis_index] = my_matrix[12  + axis_index] * -1
    
    cmds.xform(current_object, matrix=my_matrix, worldSpace=1, absolute)


def mirror(current_object, mirror_axis = 'x'):
    
    if not current_objects:
        current_objects = cmds.ls(sl = True)[0]
    axis_list = "xyz"
