'''
Created on Mar 10, 2014

@author: anamei92
'''

import pymel.core as pm
from utils import nameUtils, xformUtils

class Control(object):
    def __init__(self, side = "C", baseName = "control", size = 1, objColor = "yellow", aimAxis = "x", typeControl = "normal"):
        '''
        Contructor to create controls
        
        @param:[in] baseName : this the name that will be used as default
        @param:[in] side: this is the default side
        @param:[in] size: this the default size
        @param:[in] objColor: string that specify the color of the chain
        @param:[in] aimAxis : this is the aim axis used to orient the control, 
        use only vector for x,y,z and their negatives 
        '''
        
        self.baseName = baseName
        self.side = side
        self.size = size
        self.objColor = objColor
        self.aimAxis = aimAxis
        #checks if the control is a PV control
        self.typeControl = typeControl
        
        #the zeroed out control and its parent group
        self.control = None
        self.controlGrp = None
        self.controlName = None
        
    def circleCnt(self):
        '''
        Creates a circle control
        '''
        self.__buildName()
        if self.controlName:
            self.control = pm.circle(name = self.controlName, ch = 0, o=1 , nr=[1,0,0])[0]
        
        self.__finalizeCnt()
        
    
    def pinCnt(self):
        '''
        creates a pin control
        '''
        
        self.__buildName()
        if not self.controlName:
            return
        line = pm.curve(d = 1, p = [(0,0,0), (0.8,0,0)], k = [0,1], n = self.controlName)
        circle = pm.circle(ch=1, o = True, nr = (0, 1, 0), r = 0.1)[0]
        
        pm.move(0.9, 0, 0, circle.getShape().cv, r = 1)
        pm.parent(circle.getShape(), line, shape = 1, add = 1)
        
        pm.delete(circle)
        pm.select(cl=1)
        self.control = line
        
        self.__finalizeCnt()
        
    def boxCnt(self):
        '''
        creates a box control
        '''
        self.__buildName()
        if not self.controlName:
            return
        length = 0.1
        pointsTop = [(length,length*2,length), (length,length*2,-length),(-length,length*2,-length), (-length,length*2,length),(length,length*2,length) ]
        pointsBot = [(length,0.0,length), (length,0.0,-length),(-length,0.0,-length), (-length,0.0,length),(length,0.0,length) ]
       
        line = pm.curve(d = 1, p = [(length,0,length), (length,length*2,length)], n = self.controlName)
        other = pm.curve(d = 1, p = [(length,0,-length), (length,length*2,-length)], n = self.controlName)
        pm.parent(other.getShape(), line, shape = 1, add = 1 )
        pm.delete(other)
        other = pm.curve(d = 1, p = [(-length,0,-length), (-length,length*2,-length)], n = self.controlName)
        pm.parent(other.getShape(), line, shape = 1, add = 1 )
        pm.delete(other)
        other = pm.curve(d = 1, p = [(-length,0,length), (-length,length*2,length)], n = self.controlName)
        pm.parent(other.getShape(), line, shape = 1, add = 1 )
        pm.delete(other)
        other = pm.curve(d = 1, p = pointsTop, n = self.controlName)
        pm.parent(other.getShape(), line, shape = 1, add = 1 )
        pm.delete(other)
        other = pm.curve(d = 1, p = pointsBot, n = self.controlName)
        pm.parent(other.getShape(), line, shape = 1, add = 1 )
        pm.delete(other)
        pm.select(cl=1)
#         
        self.control = line
            
        self.__finalizeCnt()
        
    def sphereCnt(self):
        '''
        create a sphere control
        '''
        self.__buildName()
        if self.controlName:
            circle = pm.circle(name = self.controlName, ch = 0, o=1 , nr=[1,0,0], r = 0.1)[0]
            circley = pm.circle(name = self.controlName, ch = 0, o = True, nr = [0, 1, 0], r = 0.1)[0]
            pm.parent(circley.getShape(), circle, shape = 1, add = 1 )
            pm.delete(circley)
            circlez = pm.circle(name = self.controlName, ch = 0, o = True, nr = [0, 0, 1], r = 0.1)[0]
            pm.parent(circlez.getShape(), circle, shape = 1, add = 1 )
            pm.delete(circlez)
            self.control = circle
            for s in self.control.getShapes():
                pm.move(0, 0.1, 0, s.cv, r=1)
        self.__finalizeCnt()
    
        
    def __finalizeCnt(self):
        '''
        Adjusting the control orientation, scales, and zeroing 
        '''
        self.__aimCnt()

        if self.size != 1:
            for s in self.control.getShapes():
                pm.scale(s.cv, self.size,self.size,self.size, r=1)
            #delete history on the scaled control     
            pm.delete(self.control, ch =1)
        self.setColor(self.control, self.objColor)
        self.controlGrp = xformUtils.zero(self.control)

    def __buildName(self):
        '''
        creates a unique name for the control
        '''
        if self.typeControl != "PV":
            self.controlName = nameUtils.getUniqueName(self.side, self.baseName, "CNT")
        elif self.typeControl == "PV":
            addedName = self.baseName + "PV"
            self.controlName = nameUtils.getUniqueName(self.side, addedName, "CNT")
    
    def __aimCnt(self):
        '''
        corectly aims the control according to the proper aim axis
        '''
        y = 0
        z = 0
        
        if self.aimAxis == "y":
            z = 90
        elif self.aimAxis == "z":
            y = -90
        
        for s in self.control.getShapes():
            pm.rotate(s.cv, 0, y, z, r=1) 
    
    def setColor(self, control, color):
        '''
        Changes the color of the control
        @param: control
        @param: color to change to
        '''
        colorNum = 0
        if self.objColor == "yellow":
            colorNum = 17
        elif self.objColor == "red":
            colorNum = 13
        elif self.objColor == "blue":
            colorNum = 6
            
        for s in self.control.getShapes():
            s.overrideEnabled.set(True)
            s.overrideColor.set(colorNum)

    