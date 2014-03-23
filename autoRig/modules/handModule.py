
import pymel.core as pm
from subModules import fkChain,ikChain, boneChain
from utils import nameUtils




class HandModule(object):
    
    posHandArray = [[9.776212928181883, 6.370783677812179, 0.4755996745899158],[10.127,6.128,0.951]]
    rotHandArray = [[29.067, -9.816778333290632, -44.065]]
    
    
    def __init__(self, side = "L", baseName ="hand", ctlSize =1, ctlColor = "yellow" ):
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


        self.thumbPosArray = []
        self.thumbRotArray = []   
        self.indexPosArray = []
        self.indexRotArray = []
        self.middlePosArray = []
        self.middleRotArray = []
        self.ringPosArray = []
        self.ringRotArray = []
        self.pinkiePosArray = []
        self.pinkieRotArray = []


    def build(self):
        
        self.handChain = fkChain.FkChain(self.side, self.baseName)
        self.handChain.fromList(self.posHandArray,self.rotHandArray)
        
        
        self.buildThumb()
        self.buildIndex()
        self.buildMiddle()
        self.buildRing()
        self.buildPinkie()
        
  


        self.__cleanUp()

        
    
    
    def buildThumb(self):
        
        pm.select (cl=1)
        self.thumbChain = fkChain.FkChain(self.side, "thumb")
        
        
        self.thumbPosArray = [[9.654,5.862,1.363],[9.541,5.635,1.77],[9.535,5.309,2.147]]
        self.thumbRotArray = [[154.794,-59.445,-91.054],[169.494,-56.845,-99.254],[154.794,-59.445,-91.054]]
        self.thumbChain.fromList(self.thumbPosArray,self.thumbRotArray)
        
    def buildIndex (self):
        
        pm.select (cl=1)
        self.indexChain = fkChain.FkChain(self.side, "index")
        
        self.indexPosArray = [[10.198,5.611,1.934],[10.372,5.268,2.376],[10.582,4.881,2.833],[10.799,4.514,3.211]]
        self.indexRotArray = [[154.794,-59.445,-91.054],[169.494,-56.845,-99.254],[154.794,-59.445,-91.054]]
        self.indexChain.fromList(self.indexPosArray,self.indexRotArray)
        
    def buildMiddle (self):
        
        pm.select (cl=1)
        self.middleChain = fkChain.FkChain(self.side, "middle")
        
        self.middlePosArray = [[10.724,5.555,1.739],[11.075,5.144,2.135],[11.362,4.776,2.519],[11.667,4.389,2.882]]
        self.middleRotArray = [[154.794,-59.445,-91.054],[169.494,-56.845,-99.254],[154.794,-59.445,-91.054]]
        self.middleChain.fromList(self.middlePosArray,self.middleRotArray) 
        
    def buildRing (self):
        
        pm.select (cl=1)
        self.ringChain = fkChain.FkChain(self.side, "ring")
        
        self.ringPosArray = [[11.138,5.528,1.343],[11.498,5.196,1.647],[11.819,4.841,1.911],[12.155,4.509,2.169]]
        self.ringRotArray = [[154.794,-59.445,-91.054],[169.494,-56.845,-99.254],[154.794,-59.445,-91.054]]
        self.ringChain.fromList(self.ringPosArray,self.ringRotArray) 
        
    
    def buildPinkie (self):
        
        pm.select (cl=1)
        self.pinkieChain = fkChain.FkChain(self.side, "pinkie")
        
        self.pinkiePosArray = [[11.256,5.556,0.876],[11.65,5.265,1.067],[12.028,4.929,1.231],[12.398,4.628,1.41]]
        self.pinkieRotArray = [[154.794,-59.445,-91.054],[169.494,-56.845,-99.254],[154.794,-59.445,-91.054]]
        self.pinkieChain.fromList(self.pinkiePosArray,self.pinkieRotArray) 
        
        
    def __cleanUp(self):
        
        for i in (self.thumbChain.chain, self.indexChain.chain, self.middleChain.chain, self.ringChain.chain,self.pinkieChain.chain):
            iJoint = i[0].name()
            pm.parent(iJoint,self.handChain.chain[-1].name() )
        
        self.bonesGrp = pm.group (empty = 1, n= nameUtils.getUniqueName(self.side, self.baseName + "Bones", "GRP"))
        self.bonesGrp.setMatrix(self.handChain.chain[0].wm.get())
  
        self.handChain.chain[0].setParent(self.bonesGrp)
        
        self.ctlsGrp = pm.group (self.handChain.controlsArray[0].controlGrp, 
                                 self.thumbChain.controlsArray[0].controlGrp,
                                 self.indexChain.controlsArray[0].controlGrp, 
                                 self.middleChain.controlsArray[0].controlGrp,
                                 self.ringChain.controlsArray[0].controlGrp,
                                 self.pinkieChain.controlsArray[0].controlGrp, 
                                 n= nameUtils.getUniqueName(self.side, self.baseName + "Controls", "GRP"))
        
        self.mainGrpLimb = pm.group (empty= 1, n= nameUtils.getUniqueName (self.side, self.baseName + "Main", "GRP"))
        
        for o in (self.bonesGrp, self.ctlsGrp):
            o.setParent(self.mainGrpLimb)
        
        for i in (self.thumbChain.controlsArray[0].controlGrp,self.indexChain.controlsArray[0].controlGrp,self.middleChain.controlsArray[0].controlGrp,self.ringChain.controlsArray[0].controlGrp,self.pinkieChain.controlsArray[0].controlGrp):
            pm.parent(i, self.handChain.controlsArray[0].controlName)

        
        