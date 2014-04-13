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
    
    def __init__(self, laplacianWt, laplacianScale, 
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
        
    def build(self, mesh):
                        
        #create a duplicated of the current mesh
        self.mesh = mesh.duplicate(n="smoothedMesh")[0]
        #element count
        self.numVerts = len(self.mesh.vtx)
        self.numFaces = len(self.mesh.faces)
        
#         print "numVerts = " + str(self.numVerts)
#         print "numFaces = " + str(self.numFaces)
        self.originalFaceArea = {}
        
        self.surfaceArea = meshUtils.surfaceArea(self.mesh, self.originalFaceArea)
        self.volume = meshUtils.volume(self.mesh)
        
        print "total Area = " + str(self.surfaceArea)
        print "volume = "+ str(self.volume)
          
        self.lapConstraintWt = 1.0/ (10.0 * math.sqrt(self.surfaceArea/self.numFaces))
        print "Laplacian Constraint Weight = " + str(self.lapConstraintWt)
         
#         #store the vertex weight for each vertex
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
        
        #something about transforming collapsed vertices
        #multiply by scaleFactor
    
    def geometryCollapse(self, maxIter = 10):
        '''
        This process is responsible for the mesh contraction step
        '''
        print "geometry collapsed"
        currVolume = 50.0
        currArea = 0.0
        currIter = 0
 
        while currIter < maxIter and currVolume/self.volume > volumeRatioEpsilon:
#             A = self.__buildMatrixA()
#             #is this how you get transposed?
#             ATA = A.transpose() * A
#              
#             #apply implicit smooth operation
#             self.__implicitSmooth()
#              
#             #compute new mesh volume
#             currVolume = meshUtils.volume(self.mesh)
#              
#             #compute new mesh area
#             currArea = meshUtils.area(self.mesh)
             
            #done with current iteration
            currIter += 1
        print "NumIter = " + str(currIter)
            
            
    def __buildMatrixA(self):
        print "building matrix"
        matA = pmu.MatrixN(range(0,1), shape = (3*self.numVerts,self.numVerts))
#  a       print matA.formated
        areaRatio = {}
        collapsed = {}
        
        MAX_POS_WEIGHT = 10000
        MAX_LAP_WEIGHT = 2000
        
        #for each face on mesh, computer areas and cotangents
        for each in self.mesh.faces:
            #calcuate new face area
            areaRatio[each] = each.getArea()/ self.originalFaceArea[each]
            
            #get points of the face
            #world?? preTransform??
            v1 = each.getPoint(0)
            v2 = each.getPoint(1)
            v3 = each.getPoint(2)
        
    def __implicitSmooth(self):
        print "performing implicit smooth"
    
    def simplification(self):
        print "simplifying"
 
    def embeddingImproving(self):
        print "improving embedding"
        
        
    def setupAdjacencyList(self):
        '''
        This method find the adjacent vertices and faces of each vertex and store them
        in dictionary
        '''
        for n in self.mesh.vtx:
            self.adjVerts[n] = n.connectedVertices()
            self.adjFaces[n] = n.connectedFaces()

      
        
            
        
        
        