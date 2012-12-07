import maya.cmds as cmds

#TO-DO----------------create window that will allow to separately grab the IK jnts and the ctrl joints
#TO-DO----------------control joints get identified, make a control for each (import zbw_rig) and parent constr the joints to the controls. Then bind the curve (rename it!) to the control joints. then figure out (parentConstr?) the loc groups to the joints
#TO-DO----------------bind the spline to the control joints
#TO-DO----------------hook up the ik joints to the control setup (parent constraints? )

def divineSpineUI():
	widgets = {}
	if cmds.window("splineWin", exists=True):
		cmds.deleteUI("splineWin")
	widgets["win"] = cmds.window("splineWin", t="Spline Maker", w=300, h=200)
	widgets["columnLO"] = cmds.columnLayout()
	widgets["getIKJntsBut"] = cmds.button(l="Get IK Jnts", w= 300, h=50, bgc=(.5, .5, .5), c=splineIK)
	widgets["getCtrlJntsBut"] = cmds.button(l="Get CTRL Jnts", w=300, h=50, bgc = (.5, 0, 0))

	cmds.showWindow(widgets["win"])

def splineIK(*args):
	tempIKJnts = []
	tempBindJnts = []
	bindJnts = []
	ikJnts = []
	ctrlJnts = []
	ikHandles = []
	locList = []
	groupList = []
	curve = ""

	#select top joint of chain for IK
	all = cmds.select(hi=True)
	rawJnts = cmds.ls(sl=True, type="joint")

	#rename to "bind"
	for jnt in rawJnts:
		if cmds.listRelatives(jnt, p=True):
			cmds.parent(jnt, w=True)
		thisRaw = cmds.rename(jnt,"bind_%02d_JNT"%(rawJnts.index(jnt)))
		tempBindJnts.append(thisRaw)


	for x in range(len(tempBindJnts)):
		thisIkRaw = cmds.duplicate(tempBindJnts[x])
		newName = "IK_%02d_JNT"%x
		thisIKJnt = cmds.rename(thisIkRaw, newName)
		tempIKJnts.append(thisIKJnt)

	for x in range(len(tempBindJnts)-1, 0, -1):
		cmds.parent(tempBindJnts[x], tempBindJnts[x-1])
		cmds.parent(tempIKJnts[x], tempIKJnts[x-1])

	cmds.select(tempBindJnts[0], hi=True)
	bindJnts = cmds.ls(sl=True, l=True)
	cmds.select(tempIKJnts[0], hi=True)
	ikJnts = cmds.ls(sl=True, l=True)

	#on IK chain create an IKRP on each jnt pointing to the next one down
	for i in range(len(bindJnts)-1):
		ikName = "%s_IKHandle"%bindJnts[i].rpartition("|")[2]
		cmds.ikHandle(n=ikName, sj=bindJnts[i], ee=bindJnts[i+1], solver="ikRPsolver" )
		cmds.parent(ikName, ikJnts[i+1])
		ikHandles.append(ikName)

	#create splineIK on IK jnts
	ikSplineName = "ikSplineHandle"
	splineIK = cmds.ikHandle(sol="ikSplineSolver", n=ikSplineName, sj=ikJnts[0], ee=ikJnts[len(ikJnts)-1])

	#on each IK joint create a loc and move it off in some direction (relative to the IKRPsolver), hook it to the IK Handle
	for j in range(len(ikHandles)):
		locName  = "pv_loc_%02d"%j
		groupName = locName + "_GRP"
		#create locator
		cmds.spaceLocator(n=locName, p=(0,0,0))
		#get joint position
		jntPos = cmds.xform(ikJnts[j], ws=True, q=True, rp=True)
		cmds.xform(locName, ws=True, t=[jntPos[0], jntPos[1]-1, jntPos[2]])
		cmds.poleVectorConstraint(locName, ikHandles[j])
		locList.append(locName)
		#create an empty group and put it at the jntPos
		cmds.group(empty=True, n=groupName)
		groupList.append(groupName)
		cmds.xform(groupName, ws=True, t=jntPos)
		#parent the locs to the groups
		cmds.parent(locName, groupName)
		#parent the groups to the ikJnts
		cmds.parent(groupName, ikJnts[j])

def controlJoints():
	pass
	#do the stuff to the control joints here