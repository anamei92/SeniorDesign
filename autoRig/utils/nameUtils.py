'''
Created on Feb 26, 2014

@author: anamei92
'''

from maya import OpenMaya, cmds
import autorig_settings

def getUniqueName(side, baseName, suffix):
    '''
    @param[in] baseName: this is the baseName of the object
    @param[in] side: this is the side of the name
    @param[in] suffix: this is the suffix of the name
    @return string of new name 
    '''
    
    security = 2000
    
    if not side in autorig_settings.sides:
        OpenMaya.MGlobal.displayError("Side is not valid")
        return
    
    if not suffix in autorig_settings.suffixes:
        OpenMaya.MGlobal.displayError("Suffix is not valid")
        return
    
    name = side + "_" + baseName + "_" + str(0) + "_" + suffix
    i = 0
    while (cmds.objExists(name) == 1):
        if( i < security):
            i+=1
            
            name = side + "_" + baseName + "_" + str(i) + "_" + suffix
    if checkName(name):
        return name
    
def checkName(name):
    '''
    Check if the name is in the right format
    @param name 
    @return boolean value
    '''
    check = name.split("_")
    
    if len(check) != 4:
        return 0
    
    side = check[0]
    if not side in autorig_settings.sides:
        return 0
    
    suffix = check[3]
    
    if not suffix in autorig_settings.suffixes:
        return 0
    try:
        num = int(check[2])
    except ValueError:
        return 0
    
    return 1
