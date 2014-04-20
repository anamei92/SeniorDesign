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
nanEpsilon = 0.00001

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
        
#         print "total Area = " + str(self.surfaceArea)
#         print "volume = "+ str(self.volume)
          
        self.lapConstraintWt = 1.0/ (10.0 * math.sqrt(self.surfaceArea/self.numFaces))
#         print "Laplacian Constraint Weight = " + str(self.lapConstraintWt)
#          
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
    
    def geometryCollapse(self, maxIter = 4):
        '''
        This process is responsible for the mesh contraction step
        '''
        print "geometry collapsed"
        currVolume = 10.0
        currArea = 0.0
        currIter = 1
        
        self.A = self.__buildMatrixA()
        
        self.ATA = self.A.transpose() * self.A
        
        self.__implicitSmooth(self.ATA)
        
#         currVolume = meshUtils.volume(self.mesh)
        
        while currIter < maxIter and currVolume/self.volume > volumeRatioEpsilon:
            self.A = self.__buildMatrixA()
#             print A.formated
#             #is this how you get transposed?
            self.ATA = self.A.transpose() * self.A
#              
#             #apply implicit smooth operation
            self.__implicitSmooth(self.ATA)
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
#       print matA.formated
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
            ilist = each.getVertices()
            ind1 = ilist[0]
            ind2 = ilist[1]
            ind3 = ilist[2]
        
            v1 = self.mesh.vtx[ind1].getPosition()
            v2 = self.mesh.vtx[ind2].getPosition()
            v3 = self.mesh.vtx[ind3].getPosition()
    
            cot1 = v1.cotan(v2, v3)
            cot2 = v2.cotan(v3, v1)
            cot3 = v3.cotan(v1, v2)
    
            #check for nan 
#
            if math.isnan(cot1) or math.isnan(cot2) or math.isnan(cot3) or areaRatio[each] < surfaceAreaEpsilon:                
                cot1 = cot2 = cot3 = 0.0
#                 
            #assign values to matrix
            matA[ind2, ind2] += -cot1 
            matA[ind2, ind3] += cot1
            matA[ind3, ind3] += -cot1
            matA[ind3, ind2] += cot1
            matA[ind3, ind3] += -cot2
            matA[ind3, ind1] += cot2
            matA[ind1, ind1] += -cot2
            matA[ind1, ind3] += cot2
            matA[ind1, ind1] += -cot3
            matA[ind1, ind2] += cot3
            matA[ind2, ind2] += -cot3
            matA[ind2, ind1] += cot3
#         print matA.formated
            #perform operations on each vertex and get position constraints
        for each in self.mesh.vtx:
            totalRatio = 0.0
            index = each.indices()[0]
            #get all neighbor faces of current vertex
            for every in self.adjFaces[each]:
                totalRatio += areaRatio[every]
            totalRatio = totalRatio/len(self.adjFaces[each]) 
            
            totalPosWeight = meshUtils.matColSum(matA, index)
#             print totalPosWeight

            if totalPosWeight > MAX_POS_WEIGHT:
                
                collapsed[each] = True
                self.vertexFlag[each] = 1
                meshUtils.matColMultiply(matA, index , 1.0/MAX_POS_WEIGHT)
            
            #normalize by row sum
            meshUtils.matColMultiply(matA, index, self.lapWeights[index])
            
            #assign new weights
            self.lapWeights[index] *= self.lapScale
            self.posWeights[index] = (1.0/ (math.sqrt(totalRatio)))*self.posConstraintWt
            
            self.lapWeights[index] = min(MAX_LAP_WEIGHT, self.lapWeights[index])
            self.posWeights[index] = min(MAX_POS_WEIGHT, self.posWeights[index])
        
#         print self.lapWeights[0]
        #assign positional weights
        for each in self.mesh.vtx:
            index = each.indices()[0]
            matA[index + self.numVerts, index] = self.posWeights[index]
            matA[index + 2*self.numVerts, index] = self.origPosConstraintWt
        
#         print matA.formated

        return matA
    
    def __implicitSmooth(self, mat):
        print "performing implicit smooth"

        b = pmu.MatrixN(range(0,1), shape = (3*self.numVerts,3))
        
        for i in xrange(self.numVerts):
            b[i+self.numVerts, 0] = self.mesh.vtx[i].getPosition().x*self.posWeights[i]
            b[i+self.numVerts, 1] = self.mesh.vtx[i].getPosition().y*self.posWeights[i]
            b[i+self.numVerts, 2] = self.mesh.vtx[i].getPosition().z*self.posWeights[i]
        ATb = self.A.transpose()*b
        #solve for A*x = b
        
        x = self.ATA.linverse()*ATb
        
        #set the new vertices position
        for n in xrange(self.numVerts):
            point= [x[n,0], x[n,1], x[n,2]] 
            self.mesh.vtx[n].setPosition(point)
            

        
    
    
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
       
            
        