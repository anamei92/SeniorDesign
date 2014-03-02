'''
Created on Feb 26, 2014

@author: anamei92
'''

from maya import OpenMaya
import pymel.core as pm
import pymel.util as pmu
import math

#pi/180
Rad = 3.14159265359/180.0
class curveSkeleton(object):
    
    def __init__(self, obj = None):
        self.obj = obj
        #get the vertices of the mesh
        self.verts = []
        self.edges = []
        self.faces = []
        self.numVerts = 0
        self.numEdges = 0
        self.numFaces = 0
        self.averageFaceArea = 0
        self.areaRing = []
        self.W_L = None
        self.W_H = None
        self.points = []
        self.vertsPos = None
        
    def contractMesh(self,obj):
        '''
        This method performs laplace smoothing on the mesh
        @param PyNode: object to be smoothed
        '''
        
        #make a duplicate of the mesh 
        newObj = obj.duplicate(n="smoothedMesh")[0]
        
        #set variables for the initial state
        self.verts = newObj.vtx
        self.edges = newObj.edges
        self.faces = newObj.faces
        self.numVerts = len(self.verts)
        self.numEdges = len(self.edges)
        self.numFaces = len(self.faces)
        #calculate the average face area of the mesh
        for face in self.faces:
            self.averageFaceArea+= face.getArea()
        self.averageFaceArea = self.averageFaceArea/self.numFaces
        
        #calculate the one-ring area for each vertex
        for vert in self.verts:
            area = 0;
            faceRing = vert.connectedFaces()
            for face in faceRing:
                area += face.getArea()
            self.areaRing.append(area)
        
        self.W_L = pmu.MatrixN(range(0,1), shape = (self.numVerts,self.numVerts))
        self.W_H = pmu.MatrixN(range(0,1), shape = (self.numVerts,self.numVerts))
        self.vertsPos = pmu.MatrixN(range(0,1), shape = (self.numVerts,3))
        #comeback and play with this constant more
        for i in range(0,self.numVerts):
            self.W_L[i,i] = math.sqrt(self.averageFaceArea)
            self.W_H[i,i] = 1.0
            currPoint = self.verts[i].getPosition()
            self.points.append(currPoint)
            self.vertsPos[i,0] = currPoint.x
            self.vertsPos[i,1] = currPoint.y
            self.vertsPos[i,2] = currPoint.z
                
        laplaceOp = self.calculateLaplace(newObj)
        self.newVertices(laplaceOp)
    
    
    def calculateLaplace(self,obj):
        '''
        This method calculate the laplace operator
        @param PyNode: object to be smoothed
        @param int: number of iteration
        @return MatrixN of nxn where n is the number of vertices 
        '''
        #create an nxn matrix with all indices set to zero
        laplaceOp = pmu.MatrixN(range(0,1), shape = (self.numVerts,self.numVerts))
        
        #calculate the laplace operator.
        #temporaily ignoring i = j cases 
        for n in range(0,self.numVerts):
            #print n.indices()[0]
            for m in range(0,self.numVerts):
                if(n != m and laplaceOp[n,m] == 0):
                    edge = self.edgeExist(self.verts[n],self.verts[m])
                    if edge:
                        angles = self.oppositeAngles(edge)
                        #print "first angle: ", angle[0]/Rad
                        #print "second angle: ", angle[1]/Rad
                        w_ij = 1.0/math.tan(angles[0]) + 1.0/math.tan(angles[1])
                        laplaceOp[n,m] = w_ij
                        laplaceOp[m,n] = w_ij
        for n in range(0,self.numVerts):
            sumWeight = 0
            for m in range(0,self.numVerts):
                sumWeight -= laplaceOp[n,m]  
            laplaceOp[n,n] = sumWeight
                    
                    
        #print laplaceOp.formated
        
        return laplaceOp
    
    def edgeExist(self,i,j):
        '''
        This method takes in two meshVertex and check if they are an meshedge
        @param: meshVertex i
        @param: meshVertex j
        @return meshEdge if found and none if not
        '''
        edges = i.connectedEdges()
        for n in edges:
            if n.isConnectedTo(j):
                return n
        return None
    
    def oppositeAngles(self, edge):
        '''
        this method takes in one edge and get the opposite angles in radian
        @param an meshEdge
        @param the meshEdge list 
        @return list of two float 
        '''
        angles = []
        face = edge.connectedFaces()
        #print "num of faces: ", len(face)
        
        for f in face:
            indices = f.getEdges()
            #print "num of indices: ", len(indices)
            
            for n in indices:
                if edge == self.edges[n]:
                    #print "edge :", n
                    indices.remove(n)
            edgeA = self.edges[indices[0]]
            edgeB = self.edges[indices[1]]
            commonVertex = self.getCommonVertex(edgeA, edgeB)
            if commonVertex:
                angle = commonVertex.angle(edge.getPoint(0), edge.getPoint(1))
                angles.append(angle)
        return angles
    
    def getCommonVertex(self, i, j):
        '''
        This method takes in two connected meshEdges and find the common vertex
        @param: meshEdge i
        @param: meshEdge j
        @return common meshVertex
        '''
        
        #get points of edge i
        pointsi = [i.getPoint(0),i.getPoint(1)]
        pointsj = [j.getPoint(0),j.getPoint(1)]
        #i = 0
        for n in pointsi:
            if n in pointsj:
                #i+=1
                #print "found common point: ", i
                return n 
        return None
    
    def calculateW_L(self):
        '''
        This method calculate the weight matrix for contraction
        @param the matrixN W_L of the previous iteration
        @return the matrixN W_L for the current iteration
        '''
        s_l = 2.0
        self.W_L = s_l*self.W_L
    
    def calculateW_Hi(self):
        '''
        This method calculate the weight matrix for attraction
        @param the matrixN W_hi of the previous iteration
        @return the matrixN W_hi for the current iteration
        '''
        newAreas = []
        for n in range(0, self.numVerts):
            currAreaRing = 0
            connectFaces = self.verts[n].connectedFaces()
            for m in connectFaces:
                currAreaRing += m.getArea()
            newAreas.append(currAreaRing)
            newValue = self.W_H[n,n]*math.sqrt(self.areaRing[n]/currAreaRing)
            self.W_H[n,n] = newValue
        self.areaRing = newAreas
    
    def newVertices(self, laplaceOp):
        '''
        This method calculate and set the new vertices position
        '''
        matrix = self.W_L*laplaceOp
        matrix.extend(self.W_H)
        matrix = matrix.linverse()
        
        newVerts = matrix*self.vertsPos
        self.vertsPos = newVerts
        
        for i in range(0,self.numVerts):
            self.points[i].x = newVerts[i,0]
            self.points[i].y = newVerts[i,1]
            self.points[i].z = newVerts[i,2]
            self.verts[i].setPosition(self.points[i])
        