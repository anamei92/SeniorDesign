'''
Created on Feb 26, 2014

@author: anamei92
'''

from maya import OpenMaya
import pymel.core as pm
import nameUtils

def zero(obj):
    '''
    This method get a pymel object as input and group it to zero its transform
    @param: obj: PyNode, the object to zero out
    @return PyNode, the offset group
    '''
    
    #get the parent
    par = obj.getParent()
    
    #create group name
    name = obj.name()
    temp = name.split("_")
    
    groupName = nameUtils.getUniqueName(temp[0],temp[1] + "Zero", "GRP")
    if not groupName:
        OpenMaya.MGlobal.displayError("Error:Name is not valid")
        return
    
    #create the a new transform node
    grp = pm.createNode("transform", n = groupName)
    
    #set the world matrix of the group 
    grp.setMatrix(obj.wm.get())
    
    #rebuild the hierarchy
    obj.setParent(grp)
    if par:
        grp.setParent(par)

def zeroTranslate(obj):
    '''
    This method get a pymel object as input and group it to zero its transform
    @param: obj: PyNode, the object to zero out
    @return PyNode, the offset group
    '''
    
    #get the parent
    par = obj.getParent()
    
    #create group name
    name = obj.name()
    temp = name.split("_")
    
    groupName = nameUtils.getUniqueName(temp[0],temp[1] + "Zero", "GRP")
    if not groupName:
        OpenMaya.MGlobal.displayError("Error:Name is not valid")
        return
    
    #create the a new transform node
    grp = pm.createNode("transform", n = groupName)
    
    #set the world matrix of the group 
    grp.translate.set(obj.translate.get())
    
    #rebuild the hierarchy
    obj.setParent(grp)
    if par:
        grp.setParent(par)

def zeroRotate(obj):
    '''
    This method ge a pymel object as input and group it to zero its translation only
    @param: obj: PyNode, the object to zero out
    @return PyNode, the offset group
    '''
    
    #get the parent
    par = obj.getParent()
    
    #create group name
    name = obj.name()
    temp = name.split("_")
    
    groupName = nameUtils.getUniqueName(temp[0],temp[1] + "Zero", "GRP")
    if not groupName:
        OpenMaya.MGlobal.displayError("Error:Name is not valid")
        return
    
    #create the a new transform node
    grp = pm.createNode("transform", n = groupName)
    
    #set the world matrix of the group 
    grp.rotate.set(obj.rotate.get())
    
    #rebuild the hierarchy
    obj.setParent(grp)
    if par:
        grp.setParent(par)   
    
