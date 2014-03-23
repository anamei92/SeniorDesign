import pymel.core as pm

from subModules import fkChain,ikChain, boneChain
from utils import nameUtils
from modules import limbModule, handModule



class ArmModule(object):
    
    def __init__(self, side = "L", baseName ="arm", ctlSize =1, ctlColor = "yellow",solver = "ikRPsolver",controlOrient = [0,0,0]):
        '''
        This is the constructor
        @param baseName: str, the base name used to generates the names
        @param side: str, the side used to generates names
        @param ctlColor : str, what color to apply on the controls
        @param ctlSize : float, the control size
        '''
        

        self.side = side
        self.baseName = baseName
        self.ctlSize = ctlSize
        self.ctlColor = ctlColor
        self.solver = solver
        self.controlOrient = controlOrient



    def build(self):
        
        
        self.limb = limbModule.LimbModule(self.side, self.baseName,self.ctlSize,self.ctlColor,self.solver,self.controlOrient)
        self.limb.build()
        #If i want to call a procedure from an other class, is this the best way ?
        
        self.hand = handModule.HandModule()
        self.hand.build()
        
        

