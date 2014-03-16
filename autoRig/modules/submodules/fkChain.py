'''
Created on Mar 11, 2014

@author: anamei92
'''
import pymel.core as pm
import boneChain, control

class FkChain(boneChain.BoneChain):
    def __init__(self, baseName = "fkChain", side = "C", cntColor = "yellow", cntSize = 1):
        '''
        The FkChain constructor. This object inherits from the boneChain class
        @param:baseName: str, used to generate unique name
        @param: side: str, used to generate unique name
        @param:cntColor: str, color of the control
        @param:cntsSize: float, the control size 
        '''
        #initiate the parent class
        boneChain.BoneChain.__init__(self, baseName,side)
        
        #not necessarily needed since the boneChain class is already doing it
        self.baseName = baseName
        self.side = side
        
        #control attributes
        self.cntColor = cntColor
        self.cntSize = cntSize
        
        #array that store the control
        self.controlsArray = []
        
    def fromList(self, posList = [], orientList = [], autoOrient = 1, skipLast = 1):
        '''
        Builds a chain from the given position and orientation list.
        @param: posList: float[3] list, list of positions
        @param: orientList: float[3] list, list of orientations
        @param: autoOrient: bool, determines if the chain will be autoOriented
        @param: skipLast: bool, deteremines if there will be a control on the last bone
        '''       
        #call the parent class method 
        boneChain.BoneChain.fromList(self, posList, orientList, autoOrient)
        
        #add on to the parent class method
        self.__addControls(skipLast)
        self.__finalizeFkChain()
        
    def __addControls(self, skipLast = 1):
        '''
        This procedure is in charge of creating and attaching the controls of the chain
        @param: skipLast, bool, determines if there will be a control at the last bone
        '''
        
        for i in range(self.chainLength()):
            if skipLast == 1: #do nothing to the last bone if skipLast is true
                if i == (self.chainLength() - 1):
                    return
            #create a control for each bone
            cntClass = control.Control(self.side, self.baseName, self.cntSize, self.cntColor)
            cntClass.circleCnt()
            
            #snap the control to the bone by getting its world matrix
            # get the controlGrp attribute from the cntClass and ws = world space
            pm.xform (cntClass.controlGrp, ws = 1, matrix = self.chain[i].worldMatrix.get())
            #add the control into the control array
            self.controlsArray.append(cntClass)

        
    def __finalizeFkChain(self):    
        #set up control hierarchy
        reversedList = list(self.controlsArray)
        reversedList.reverse()
          
        for i in range(len(reversedList)):
            if i != (len(reversedList)-1):#if not the last control
                pm.parent (reversedList[i].controlGrp, reversedList[i+1].control)
        #orientConstraint the bone to the controls
        for i, c in enumerate(self.controlsArray):
            pm.orientConstraint(c.control, self.chain[i], mo = 1)
           
'''
Other functionalities: method that build the chain so that one control is splitting the rotation
between two controls
''' 
            