import pymel.core as pm

from subModules import fkChain,ikChain, boneChain
from utils import nameUtils



class LimbModule(object):
   
    posArray = [
                [4.44192113031648, 13.260107141970812, -1.990683606263926],
                [6.969699319574542, 8.613819224282429, -3.00179488196715],
                [9.776212928181883, 6.370783677812179, 0.4755996745899158] 
                ]
    rotArray = [
                [-19.0404555609189, 10.822010399949697, -61.451929395134634],
                [-26.483942588957117, -44.06539254514205, -38.63271862455514], 
                [-18.97739868004767, -9.816778333290632, -54.388891329740375] 
                ]
   
    
    
    def __init__(self, side = "L", baseName ="limb", ctlSize =1, ctlColor = "yellow", solver = "ikRPsolver", controlOrient = [0,0,0]):
        '''
        This is the constructor
        @param baseName: str, the base name used to generates the names
        @param side: str, the side used to generates names
        @param ctlColor : str, what color to apply on the controls
        @param ctlSize : float, the control size
        '''
        
        self.baseName = baseName
        self.side = side
        self.ctlSize = ctlSize
        self.ctlColor = ctlColor
        self.solver = solver
        self.controlOrient = controlOrient
        
        
        
        self.fkChain = None
        self.ikChain = None
        self.blendChain = None
        self.blendData = None
        
        configName = nameUtils.getUniqueName (self.side, self.baseName, "SWITCH")
        self.config_node = pm.spaceLocator(n= configName)
        
        
    def build(self):
        
        # create fk chain
        self.fkChain = fkChain.FkChain(self.side, self.baseName + "Fk", self.ctlSize, self.ctlColor)
        self.fkChain.fromList(self.posArray,self.rotArray)
        
        # create ik chain
        self.ikChain = ikChain.IkChain(self.side, self.baseName + "Ik", self.ctlSize, self.ctlColor, self.solver, self.controlOrient)
        self.ikChain.fromList(self.posArray,self.rotArray)
        
        # create the target chain
        self.blendChain = boneChain.BoneChain(self.side, self.baseName)
        self.blendChain.fromList(self.posArray,self.rotArray)


        self.blendData = boneChain.BoneChain.blendTwoChains(self.fkChain.chain,self.ikChain.chain, self.blendChain.chain, self.config_node, "FkIk", self.side, self.baseName)
        
        self.__cleanUp()
        
        
        
    def __cleanUp(self):
        
        self.bonesGrp = pm.group (empty = 1, n= nameUtils.getUniqueName(self.side, self.baseName + "Bones", "GRP"))
        self.bonesGrp.setMatrix(self.blendChain.chain[0].wm.get())
        
        for b in (self.ikChain,self.fkChain,self.blendChain):
            b.chain[0].setParent(self.bonesGrp)
            
    
        self.ctlsGrp = pm.group (self.fkChain.controlsArray[0].controlGrp, self.ikChain.ikCtl.controlGrp,self.ikChain.poleVectorCtl.controlGrp, n= nameUtils.getUniqueName(self.side, self.baseName + "Controls", "GRP"))
        
        
        self.mainGrpLimb = pm.group (empty= 1, n= nameUtils.getUniqueName (self.side, self.baseName + "Main", "GRP"))
        
        for o in (self.bonesGrp, self.ctlsGrp, self.ikChain.ikHandle,self.config_node):
            o.setParent(self.mainGrpLimb)
        
        
        
    
    

        
  
  
        
        
        
        
        
        
        
        
        
        
        
        
                