'''
Created on Apr 3, 2014

@author: anamei92
'''

import pymel.core as pm
import pymel.util as pmu
from utils import meshUtils
import math

#some static variables
volumeRatioEpsilon = 0.00001
surfaceAreaEpsilon = 0.000000001
Rad = 3.14159265359/180.0

class curveSkeleton(object):
    
    def __init__(self, mesh, laplacianWt, laplacianScale, 
                 positionWT, positionScale, origPosWt, 
                 shapeEnergyWt, simplifyRatio, jointMerge):
        '''
        @param: mesh, pyNode: the mesh that will be used to generate the curve skeleton
        @param: laplacianWT, float: weight scalar for mesh contraction
        @param: laplacianScale, float
        @param: positionWT, float 
        @param: positionScale, float
        @param: origPosWt, float
        @param: shapeEnergyWt, float
        @param: simplifyRatio, float
        @param: jointMerge, bool
        '''
        self.mesh = mesh.duplicate(n="smoothedMesh")[0]
        #initialize parameters that will be used to calculate stuff
        self.lapConstraintWt = laplacianWt
        self.posConstraintWt = positionWT
        self.origPosConstraintWt = origPosWt
        
        self.lapScale = laplacianScale
        self.posScale = positionScale
        self.shapeEnergyWt = shapeEnergyWt
        self.simplifyRatio = simplifyRatio
        self.applyJointMerge = jointMerge
        
        self.lapWeights = []
        self.posWeights = []
        self.collapsedLength = []
        self.vertexFlag = []
        
        #dictionary that stores adjacency list around a vertex
        self.adjVerts = {}
        self.adjFaces = {}
        
    def build(self):
                        
        #create a duplicated of the current mesh
        
        #element count
        self.numVerts = len(self.mesh.vtx)
        self.numFaces = len(self.mesh.faces)
        self.originalFaceArea = {}
        
        self.surfaceArea = meshUtils.surfaceArea(self.mesh, self.originalFaceArea)
        self.volume = meshUtils.volume(self.mesh)
        
        self.lapConstraintWt = 1.0/ (10.0 * math.sqrt(self.surfaceArea/self.numFaces))
        
        #store the vertex weight for each vertex
        for i in range(0, self.numVerts):
            self.lapWeights.append(self.lapConstraintWt)
            self.posWeights.append(self.posWeights)
            self.collapsedLength.append(0.0)
            self.vertexFlag.append(0)
        
        targetVertexCount = 10
        self.setupAdjacencyList()
        
        #curveSkeleton steps
        #1:
        self.geometryCollapse()
        
        #2
        self.simplification()
        
        #3
        self.embeddingImproving()
        
    
    def geometryCollapse(self, maxIter = 10):
        '''
        This process is responsible for the mesh contraction step
        '''
        currVolume = 0.0
        currArea = 0.0
        currIter = 0
        
        self.__buildMatrixA()
        
#         while True:
#             stuff()
#             if fail_condition:
#                 break
#         
    def __buildMatrixA(self):
        
        matA = pmu.MatrixN(range(0,1), shape = (3*self.numVerts,self.numVerts))
#         print matA.formated
        areaRatio = {}
        collapsed = {}
        
        MAX_POS_WEIGHT = 10000
        MAX_LAP_WEIGHT = 2000
        
        for face in self.mesh.faces:
            newFaceArea = face.getArea()
            areaRatio[face] = newFaceArea/self.originalFaceArea[face]
    
    def __implicitSmooth(self):
        pass
    
    def simplification(self):
        pass
    
    def embeddingImproving(self):
        pass
        
        
    def setupAdjacencyList(self):
        '''
        This method find the adjacent vertices and faces of each vertex and store them
        in dictionary
        '''
        for n in self.mesh.vtx:
            self.adjVerts[n] = n.connectedVertices()
            self.adjFaces[n] = n.connectedFaces()

      
        
            
        
        
        