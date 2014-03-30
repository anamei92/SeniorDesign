'''
Created on Mar 11, 2014

@author: anamei92
'''
import pymel.core as pm
import boneChain, control
from utils import nameUtils

class IkChain(boneChain.BoneChain):
    def __init__(self, baseName = "ikChain", side = "C", cntColor = "yellow", cntSize = 1, solver = "ikSCsolver", 
                 controlOrient = [0,0,0]):
        '''
        The FkChain constructor. This object inherits from the boneChain class
        @param:baseName: str, used to generate unique name
        @param: side: str, used to generate unique name
        @param:cntColor: str, color of the control
        @param:cntsSize: float, the control size 
        @param:solver: str, the solver for the IK supported value:
            - ikSCsolver : simple chain
            - ikRPsolver : rotation plain
        @param: controlOrient: float[3], the orientation applied on the control
        '''
        #initiate the parent class
        boneChain.BoneChain.__init__(self, baseName,side)
        
        #not necessarily needed since the boneChain class is already doing it
        self.baseName = baseName
        self.side = side
        
        #control attributes
        self.cntColor = cntColor
        self.cntSize = cntSize
        
        self.solver = solver
        self.controlOrient = controlOrient
        
        self.__accepteSolvers = ["ikSCsolver", "ikRPsolver"]
        
        #array that store the control
        self.grpArray = []
        self.controlsArray = []
        self.ikHandle = None
        
    def fromList(self, posList = [], orientList = [], autoOrient = 1):
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
        self.__addControls()
        self.__finalizeIkChain()
        
    def __addControls(self):
        '''
        This procedure is in charge of creating and attaching the controls of the chain
        @param: posList: float[3] list, list of positions
        '''
        #create a pv control of the bone in the middle of the chain and a regular control the end 
        for i in [self.chainLength()/2, self.chainLength() - 1]:
            
            cntClass = control.Control(self.side, self.baseName, self.cntSize, self.cntColor)
            
            #if it is the middle of the bone chain
            if i == self.chainLength()/2:
                cntClass = control.Control(self.side, self.baseName, self.cntSize, self.cntColor, typeControl = "PV")
                cntClass.sphereCnt()
            
            elif i == self.chainLength() - 1:
                #cube for hand and foot control
                cntClass.boxCnt()
            
            #snap the control group to the joint
            pm.xform(cntClass.controlGrp, ws = 1, matrix = self.chain[i].worldMatrix.get())
            
            self.grpArray.append(cntClass.controlGrp)
            self.controlsArray.append(cntClass)
    
    
    def __finalizeIkChain(self):
        '''
        Create the ikHandle and the constraints to the control
        '''
        #create ikHandle
        ikHandleName = nameUtils.getUniqueName(self.side, self.baseName, "IK")
        self.ikHandle  = pm.ikHandle(n = ikHandleName, sj = self.chain[0], ee = self.chain[-1], solver = "ikRPsolver")[0]
        #create parent constraint from the ikHandle to the last control
        pm.pointConstraint(self.controlsArray[-1].control, self.ikHandle, mo = 1)
        #create a pole vector control
        pm.poleVectorConstraint(self.controlsArray[0].control, self.ikHandle)