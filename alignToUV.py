import maya.cmds as cmds
import maya.OpenMaya as om

#use the u and v position to position and align an object to that part of the surface

pos = cmds.pointOnSurface("nurbsPlane1", u=0.5, v=0.5, position=True)
posVec = om.MVector(pos[0], pos[1], pos[2])
cmds.xform("pCube1", ws=True, t=pos)

#get tangent in the right direction (u or v)
tanv = cmds.pointOnSurface("nurbsPlane1", u=0.5, v=0.5, tv=True)

nc = cmds.normalConstraint("nurbsPlane1", "pCube1", aimVector=(0,0,1), worldUpVector=(tanv))

#normalConstraint -weight 1 -aimVector 0 0 -1 -upVector 0 1 0 -worldUpType "vector" -worldUpVector 0 1 0;
cmds.delete(nc)