#create the joints in a chain and orient them, THEN unparent them for the bind joints in the ribbon
import maya.cmds as mc
import maya.mel as mel

numJoint=5
nbName= "thisNURBS"
nbAxis=[0,0,1]
extraJntDir = [0,1,0]
ribbonName = "spine"
upVector= (1,0,0)
ribbonWidth=2
ribbonRatio=5
ribbonLength = (ribbonRatio*ribbonWidth)
ribbonStart=-5
ribbonEnd=5
aimVector=[0, -1, 0]
aimVectorOpp=[0,1,0]
aimUpVector=[1,0,0]
aimUpVectorOpp=[-1,0,0]
baseCtrlJnt = "base_" + ribbonName + "_CTRL_JNT"
midCtrlJnt = "mid_" + ribbonName + "_CTRL_JNT"
topCtrlJnt = "top_" + ribbonName + "_CTRL_JNT"
baseJnt2 = "base2Jnt"+ribbonName+"_CTRL_JNT"
topExtraJnt = "extra_"+ribbonName + "_CTRL_JNT"

def zbw_groupOrient_py():
	sel = mc.ls (sl=True)
	constrainee = sel[0]
	constrained = sel[1]
	pcName=constrainee + "PC"
	ocName=constrainee + "OC"
	groupName = constrained + "_GRP"
	mc.select (constrained, r=True)
	mc.group (n=groupName)
	mc.pointConstraint (constrainee, groupName, n=pcName)
	mc.orientConstraint (constrainee, groupName, n=ocName)

	mc.delete (pcName)
	mc.delete (ocName)
	mc.select (cl=True)

#create the nurbs plane
mc.nurbsPlane (ax=nbAxis, w=ribbonWidth, lr=ribbonRatio, d=3, u=1, v=numJoint, ch=1, n=nbName)
mc.rebuildSurface (nbName, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kc=0, su=1, du=1, sv=numJoint, dv=3, tol=0.1, fr=0, dir=0)
mc.select (nbName, r=True)
mc.delete (ch=True)
numJointS = str (numJoint)
hairData = "createHair 1 " + numJointS + " 10 0 0 0 0 5 0 1 1 1"
mel.eval (hairData)

mc.select("hairSystem*", r = True)
mc.select("pfxHair*", tgl=True)
mc.select ("*Follicles", d = True)
folGrpName = (ribbonName + "_follicle_GRP")
mc.rename ("hairSystem1Follicles", folGrpName)
#select the children of the follicles and add them to selection
mc.delete()

#rename hairSystem1Follicles
#create Joints
mc.select (nbName + "*Follicle*")
folList = mc.ls (sl =True, tr=True)

for i in range((numJoint-1), -1, -1):
	#THESE JOINTS ARE NUMBERED BACKWARDS
	#get position of follicle 1?
	mc.select (folList[i], r=True)
	mc.pickWalk (d="down")
	mc.pickWalk (d="left")
	mc.delete ()
	mc.select (folList[i], r=True)
	thisNum= ((numJoint-1)-i)
	j = str(thisNum)
	newFolName = (ribbonName + "ribbonFol_" + j)
	#print i
	mc.rename(folList[i], newFolName)
	folPos = mc.pointPosition(newFolName+".rotatePivot")
	jntName = (ribbonName + "_BIND_JNT_" + j)
	mc.joint (n=jntName ,p = folPos)
	mc.select (clear=True)

'''
#connect joints together?
numTopJoint=(numJoint-1)
for i in range (numTopJoint, 0, -1):
	j = str(i)
	k=str(i-1)
	childName = (ribbonName + "_BIND_JNT_" + j)
	parentName = (ribbonName + "_BIND_JNT_" + k)
	#parent joints together
	mc.parent (childName, parentName)

#orient joints in correct direction
mc.pickWalk (d='up')
mc.select (hi=True)
mc.joint (e=True, oj = "xyz", secondaryAxisOrient = "yup")
#unparent joint

for b in range (numTopJoint, 0, -1):
	c= str(b)
	mc.parent ((ribbonName +"_BIND_JNT_" + c), w=True)
#parent each joint to the correct follicle
'''
#the end of the nurbs plane is the axis w/ value of half length
#create Top Loc
topUp0CV = mc.pointPosition (nbName+".cv[0][0]", w=True)
topUp1CV = mc.pointPosition (nbName+".cv[1][0]", w=True)
topAimLocPos = ((topUp0CV[0] + topUp1CV[0])/2, (topUp0CV[1] + topUp1CV[1])/2, (topUp0CV[2] + topUp1CV[2])/2)
topUpLocPos = ((topAimLocPos[0] + upVector[0]), (topAimLocPos[1] + upVector[1]), (topAimLocPos[2] + upVector[2]))
topAimLocName = ribbonName + "_top_AIM_LOC"
topUpLocName = ribbonName + "_top_UP_LOC"
mc.spaceLocator (n=topAimLocName, p=topAimLocPos)
mc.xform (cp=True)
mc.delete (ch=True)
mc.spaceLocator (n=topUpLocName, p=topUpLocPos)
mc.xform (cp=True)
mc.delete (ch=True)
#CREATE EXTRA JOINT IN CONTINUATION OF TOP (OFFSET BASED ON DIRECTION OF CURVE)

#create base Locator
v=(numJoint +2)
w=str(v)
baseUp0CV = mc.pointPosition (nbName+".cv[0]["+w+"]", w=True)
baseUp1CV = mc.pointPosition (nbName+".cv[1]["+w+"]", w=True)
baseAimLocPos = ((baseUp0CV[0] + baseUp1CV[0])/2, (baseUp0CV[1] + baseUp1CV[1])/2, (baseUp0CV[2] + baseUp1CV[2])/2)
baseUpLocPos = ((baseAimLocPos[0] + upVector[0]), (baseAimLocPos[1] + upVector[1]), (baseAimLocPos[2] + upVector[2]))
baseAimLocName = ribbonName + "_base_AIM_LOC"
baseUpLocName = ribbonName + "_base_UP_LOC"
mc.spaceLocator (n=baseAimLocName, p=baseAimLocPos)
mc.xform (cp=True)
mc.spaceLocator (n=baseUpLocName, p=baseUpLocPos)
mc.xform (cp=True)
mc.delete (ch=True)
#create mid Locator
midAimLocPos = ((baseAimLocPos[0]+topAimLocPos[0])/2, (baseAimLocPos[1]+topAimLocPos[1])/2, (baseAimLocPos[2]+topAimLocPos[2])/2)
midUpLocPos = ((midAimLocPos[0] + upVector[0]), (midAimLocPos[1] + upVector[1]), (midAimLocPos[2] + upVector[2]))
midAimLocName = ribbonName + "_mid_AIM_LOC"
midUpLocName = ribbonName + "_mid_UP_LOC"
mc.spaceLocator (n=midAimLocName, p=midAimLocPos)
mc.xform (cp=True)
mc.delete (ch=True)
mc.spaceLocator (n=midUpLocName, p=midUpLocPos)
mc.xform (cp=True)
mc.delete (ch=True)

mc.select (clear=True)

#create joints at ends and middle for binding nurbs to
baseJntPos = baseAimLocPos
midJntPos = midAimLocPos
topJntPos = topAimLocPos
baseJnt2Pos = ((baseAimLocPos[0]+(extraJntDir[0]*(-1))), (baseAimLocPos[1]+(extraJntDir[1]*(-1))),(baseAimLocPos[2]+(extraJntDir[2]*(-1))))
topExtraJntPos = ((topAimLocPos[0] + extraJntDir[0]), (topAimLocPos[1] + extraJntDir[1]), (topAimLocPos[2] + extraJntDir[2]))

mc.select (cl=True)

mc.joint (n=baseCtrlJnt, p=baseJntPos)
mc.joint (n=baseJnt2, p=baseJnt2Pos)
mc.joint (n=midCtrlJnt, p=midJntPos)
mc.joint (n=topCtrlJnt, p=topJntPos)
mc.joint (n=topExtraJnt, p=topExtraJntPos)
mc.joint (baseCtrlJnt, e=True, zso=True, ch=True, oj='xyz', sao='yup')
#mc.select (cl=True)
#mc.joint (midCtrlJnt, e=True, zso=True, oj="xyz", sao="yup")
#mc.select (cl=True)
#mc.joint (topCtrlJnt, e=True, zso=True, oj="xyz", sao="yup")
mc.parent (midCtrlJnt, w=True)
mc.parent (topCtrlJnt, w=True)

#parent and move around controls groups and locators
baseCtrl = (ribbonName + "base_CTRL")
midCtrl = (ribbonName + "mid_CTRL")
topCtrl = (ribbonName + "top_CTRL")

mc.circle (n=baseCtrl, c=(0,0,0), nr=(1,0,0), sw=360, r=ribbonWidth, s=12, ch=0)
mc.circle (n=midCtrl, c=(0,0,0), nr=(1,0,0), sw=360, r=ribbonWidth, s=12, ch=0)
mc.circle (n=topCtrl, c=(0,0,0), nr=(1,0,0), sw=360, r=ribbonWidth, s=12, ch=0)

#group orient those controls to the joints just created
mc.select (baseCtrlJnt, r=True)
mc.select ((ribbonName+"base_CTRL"), tgl=True)
zbw_groupOrient_py()
'''
#groupOrientBase
sel = mc.ls (sl=True)
constrainee = sel[0]
constrained = sel[1]
pcName=constrainee + "PC"
ocName=constrainee + "OC"
groupName = constrained + "_GRP"
mc.select (constrained, r=True)
mc.group (n=groupName)
mc.pointConstraint (constrainee, groupName, n=pcName)
mc.orientConstraint (constrainee, groupName, n=ocName)

mc.delete (pcName)
mc.delete (ocName)
mc.select (cl=True)
'''
#next MID CTRL
mc.select (midCtrlJnt, r=True)
mc.select ((ribbonName+"mid_CTRL"), tgl=True)
zbw_groupOrient_py()

#next TOP CTRL
mc.select (topCtrlJnt, r=True)
mc.select ((ribbonName+"top_CTRL"), tgl=True)
zbw_groupOrient_py()

mc.parent (topAimLocName, topCtrl)
mc.parent (topUpLocName, topCtrl)

mc.parent (midAimLocName, midCtrl)
mc.parent (midUpLocName, midCtrl)

mc.parent (baseAimLocName, baseCtrl)
mc.parent (baseUpLocName, baseCtrl)


mc.parent (topCtrlJnt, topAimLocName)
mc.parent (midCtrlJnt, midAimLocName)
mc.parent (baseCtrlJnt, baseAimLocName)

#SET UP AIM CONTRAINTS FOR TOP and BOTTOM
"""
mc.aimConstraint (topCtrl, baseAimLocName, aim=aimVector, wut="objectrotation", u=aimUpVector, wu=aimUpVector, wuo=baseUpLocName)
mc.aimConstraint (baseCtrl, topAimLocName, aim=aimVectorOpp, wut="objectrotation", u=aimUpVector, wu=aimUpVector, wuo=topUpLocName)
"""
#smoothbind nurbsSurface to the ctrl joints
mc.select (baseCtrlJnt, r=True)
mc.select (midCtrlJnt, tgl=True)
mc.select (topCtrlJnt, tgl=True)
mc.select (nbName, tgl=True)

mc.skinCluster (tsb=True, mi=2, omi=True)




#hide the ctrl joints and the locators
hideList = (topAimLocName, topUpLocName, midAimLocName, midUpLocName, baseAimLocName, baseUpLocName)
for i in (hideList):
	mc.hide (i)
	mc.select (cl=True)

mc.select (nbName, r=True)
mc.select (folGrpName, add=True)
mc.group (n=(ribbonName+"_ribbonWorld_GRP"), w=True)

mc.select ((baseCtrl + "_GRP"), add=True)
mc.select ((midCtrl + "_GRP"), add=True)
mc.select ((topCtrl + "_GRP"), add=True)
mc.group (n=(ribbonName+"_ribbon_GRP"), w=True)

#NAME THE CONTROLS THAT EXIST "IK"
#ADD FK CONTROLS? OR DOES THAT HAVE TO BE LEFT TO THE USER?
#ADD CONTROLS TO EACH OF THE THREE NURBS CURVES TO TURN ON/OFF THE AIM CONSTRAINT (THE MID CURVE SHOULD GET THE POINT CONSTRAINT ON/OFF. OH AND MAKE THAT PC:))
