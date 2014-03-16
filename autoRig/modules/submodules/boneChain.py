'''
Created on Mar 11, 2014

@author: anamei92
'''
import pymel.core as pm
from utils import nameUtils

class BoneChain(object):
    def __init__(self, baseName = "chain", side = "C"):
        '''
        The constructor for the bone chain
        @param: baseName: str, the base name used to generate the names
        @param: side: str, the side used to generate names
        '''
        self.baseName = baseName
        self.side = side
        
        #the array holding the created bones
        self.chain = []
        
    def fromList (self, posList =[], orientList =[], autoOrient = 1):
        '''
        This methods creates the bone in the bone chain according to the
        given position and orientation list.
        @param: posList: float[3] list, the position list for the bone chain
        @param: orientList: float[3] list, the orientation of the bones 
        @param: bool, determines if orientList will be used
        '''
        
        #traverse through the position list and create a bone for each member
        for i in range(len(posList)):
            
            #build a unique name for each bone
            tempName = nameUtils.getUniqueName(self.side, self.baseName, "JNT")
            
            #clear selection in maya to prevent unneccessary parenting of joints
            pm.select(cl=1)
            
            #creating the joints depending on autoOrient bool
            if autoOrient ==1: 
                tempJnt = pm.joint(n = tempName, position = posList[i])
            else:
                tempJnt = pm.joint(n = tempName, position = posList[i], orientation = orientList[i])
            
            #add the newly created joints into the bone chain    
            self.chain.append(tempJnt)
      
        self.__parentJoints()
          
        if autoOrient == 1:
            #oj = the first letter is the axis pointing to child and 
            #the secondary axis determines that y points up
            #maya's method to auto orient
            pm.joint(self.chain[0].name(), e = 1, oj = "xyz", secondaryAxisOrient ="yup", ch = 1, zso = 1)
          
        self.__zeroOrientJoint(self.chain[-1])
        
    def __str__(self):
        '''
        Customize print for class object
        '''
        result = "BoneChain class, length: {l} , chain : ".format(l=self.chainLength())
        chainNames = [obj.name() for obj in self.chain] 
        result += str(chainNames)
        return result
        
    def chainLength(self):
        '''
        returns how many bones are in the bone chain
        '''
        return len(self.chain)
          
    def __zeroOrientJoint(self, bone):
        '''
        Zeros out the joint Orient attributes of a bone
        @param: bone: pynode,the bone that's going to be zeroed out
        '''
        for i in ["jointOrientX", "jointOrientY", "jointOrientZ"]:
            bone.attr(i).set(0)
              
      
    def __parentJoints(self):
        '''
        parent the the joints in the bone chain accordingly
        '''
        #reverse the list by making a copy and then calling reverse()
        reversedList = list(self.chain)
        reversedList.reverse()
          
        for i in range(len(reversedList)):
            if i != (len(reversedList)-1):#if not the last bone
                pm.parent (reversedList[i], reversedList[i+1])