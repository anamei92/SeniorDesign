'''
Created on Mar 9, 2014

@author: anamei92
'''
from maya import OpenMaya
import pymel.core as pm
import pymel.util as pmu
import math

class meshSimplification(object):
    
    def __init__(self, obj):
        self.obj = obj
        #get the vertices of the mesh
        self.verts = []
        self.edges = []
        self.faces = []
        
        
    def connectiveSurgery(self,obj):
        '''
        This method is to perform the half edge collapse method
        @param: mesh to be simplified as a pynode
        @return: the simplified mesh
        '''
        self.verts = obj.vtx