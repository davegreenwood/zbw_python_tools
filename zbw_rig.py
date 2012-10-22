########################
#file: zbw_rig.py
#author: zeth willie
#contact: zeth@catbuks.com, www.williework.blogspot.com, https://github.com/zethwillie
#date modified: 09/23/12
#
#notes: helper scripts for rigging
########################

import maya.cmds as cmds
import math
import maya.OpenMaya as om

def getTwoSelection():
	"""gets two objects (only) from selection and returns them in selected order as a tuple"""
	objs = cmds.ls(sl=True)
	if len(objs) != 2:
		first,second = "empty", "empty"
		cmds.error("you haven't selected two objects")
	return objs

def getSelection():
	"""gets selected objs and returns a tuple of selections in order"""
	objs = cmds.ls(sl=True)
	return objs

def jointFromList(xformList=[], orient="xyz", secAxis="zup", strip="", suffix="", *args):
    """
    uses the xformlist arg to create a joint chain in order.
    Arguments: xformList (a list), orient ("xyz", etc), secAxis ("xup", "zdown", etc), strip (string to strip off), suffix (string to add to the joints)
    """
    jointList = []

    #if no list is provided, get the list from selection order
    if not xformList:
        sel = getSelection()

        if sel:
            xformList = sel
        #if no list && no selection then throw error
        else:
            cmds.error("you must provide a list of transforms or have the transforms selected in order")

    #clear selection
    cmds.select(cl=True)
    #for each thing in the list create a joint at that location (they'll be parented to the previous)
    for xform in xformList:
        xformPos = cmds.xform(xform, q=True, ws=True, t=True)
        jointName = "%s%s"%(xform.rstrip(strip), suffix)
        thisJoint = cmds.joint(n=jointName, p=xformPos)
        jointList.append(thisJoint)

    #now orient the joint chain based on args and return a list of the joints
    cmds.joint(jointList[0], e=True, ch=True, oj=orient, sao=secAxis)
    return(jointList)


def follicle(surface="none", folName="none", u=0.5, v=0.5, *args):
	"""
	creates a follicle on a surface based on the uv input.
	Args are: surface, folName, u, v
	"""
#------------do a bit more checking here to make sure the shapes, numbers etc work out
	if surface=="none":
		#decide if surface is polymesh or nurbsSurface
		surfaceXform = cmds.ls(sl=True, dag=True, type="transform")[0]
		surfaceShape = cmds.listRelatives(surfaceXform, shapes=True)[0]
	else:
		surfaceXform = surface
		surfaceShape = cmds.listRelatives(surfaceXform, shapes=True)[0]

	if folName == "none":
		folShapeName = "myFollicleShape"
		folXformName = "myFollicle"
	else:
		folShapeName = "%sShape"%folName
		folXformName = folName

#------------test if follicle exists
	#create the follicle
	folShape = cmds.createNode("follicle", n=folShapeName)
	folXform = cmds.listRelatives(folShape, p=True, type="transform")[0]
	cmds.rename(folXform, folXformName)

	#connect up the follicle!
	#connect the matrix of the surface to the matrix of the follicle
	cmds.connectAttr("%s.worldMatrix[0]"%surfaceShape, "%s.inputWorldMatrix"%folShape)

	#check for surface type, poly or nurbs and connect the matrix into the follicle
	if (cmds.nodeType(surfaceShape)=="nurbsSurface"):
		cmds.connectAttr("%s.local"%surfaceShape, "%s.inputSurface"%folShape)
	elif (cmds.nodeType(surfaceShape)=="mesh"):
		cmds.connectAttr("%s.outMesh"%surfaceShape, "%s.inputMesh"%folShape)
	else:
		cmds.warning("not the right kind of selection. Need a poly or nurbs surface")

	#connect the transl, rots from shape to transform of follicle
	cmds.connectAttr("%s.outTranslate"%folShape, "%s.translate"%folXform)
	cmds.connectAttr("%s.outRotate"%folShape, "%s.rotate"%folXform)

	cmds.setAttr("%s.parameterU"%folShape, u)
	cmds.setAttr("%s.parameterV"%folShape, v)

	cmds.setAttr("%s.translate"%folXform, l=True)
	cmds.setAttr("%s.rotate"%folXform, l=True)

	return(folXform, folShape)

def axisToVector(axis="+x"):
	"""
	takes an arg ("+x", "-x", "+y", "-y", "+z", "-z") and converts it to a vector (ex. (1,0,0))
	"""
	axisDict = {"+x":(1,0,0), "-x":(-1,0,0), "+y":(0,1,0), "-y":(0,-1,0), "+z":(0,0,1), "-z":(0,0,-1)}
	if axis in axisDict.keys():
		return(axisDict[axis])
	else:
		cmds.error("you need to enter an axis (i.e. '+x' or '-x'")

def fkChain(ctrlType="circle", color="red", axis="x", *args):
	"""
	puts a correctly oriented control onto each joint of selected chain. Will name the controls after the joint names and parent them according to the joint order
	Select the top joint of a chain and call fkChain(ARGS)
	Arguments: ctrlType ("sphere", "circle", "cube", etc), color ("red", "darkRed",etc. See zbw_rig.createControl for full list), axis ("x", "y", "x")
	"""

	#get the selected joint's chain of joints
	sel = cmds.ls(sl=True, type="joint")

	#initialize lists
	ctrlList = []
	groupList = []

	#for now just do one chain
	if len(sel) != 1:
		cmds.error("please select only the top level joint of one chain")
	else:
		#get the hierarchy of just joints
		allChain = cmds.select(sel[0], hi=True)
		chain = cmds.ls(sl=True, type="joint")
		chainSize = len(chain)

		for jnt in chain:
			#get the rot order
			rotOrder = cmds.getAttr("%s.rotateOrder"%jnt)

			#control name
			ctrlName =  jnt + "_CTRL"

			#create control
			ctrl = createControl(ctrlName, ctrlType, axis, color)

			#snap that control to the joint (group orient)
			groupOrient(jnt, ctrl, "GRP")
			group = ctrl + "_GRP"

			#orient constrain the joint to the control
			cmds.orientConstraint(ctrl, jnt)

			#set rotation order for the control and group
			cmds.setAttr("%s.rotateOrder"%ctrl, rotOrder)
			cmds.setAttr("%s.rotateOrder"%group, rotOrder)

			#add the controls and groups to lists to keep their order
			ctrlList.append(ctrl)
			groupList.append(group)


		#parent up the groups and controls correctly
		for i in range(chainSize-1, 0, -1):
			cmds.parent(groupList[i], ctrlList[i-1])


def createControl(name="default",type="circle", axis="x", color="darkBlue", *args):
	"""
	creates control namemed by first arg, at origin.
	shape is determined by second arg: "cube", "octogon", "sphere", "diamond", "barbell",
	third arg can be 'x',, 'y', , 'z'  and is the axis along which the control lies.
	The colors are: 'lightBlue', 'darkGreen', 'lightPurple', 'yellow', 'darkPurple', 'pink', 'blue', 'purple', 'lightGreen', 'black', 'orange', 'white', 'darkYellow', 'brown', 'lightYellow', 'darkBlue', 'royalBlue', 'darkBrown', 'lightRed', 'medBlue', 'lightBrown', 'darkRed', 'yellowGreen', 'medGreen', 'green', 'red'
	Arguments: name, type, axis, color
	"""
	colors = {}
	colors["red"]=13
	colors["blue"]=6
	colors["green"]=14
	colors["darkRed"]=4
	colors["lightRed"]=31
	colors["darkBlue"]=5
	colors["medBlue"]=15
	colors["lightBlue"]=18
	colors["royalBlue"]=29
	colors["darkGreen"]=7
	colors["medGreen"]=27
	colors["lightGreen"]=19
	colors["yellowGreen"]=26
	colors["yellow"]=17
	colors["darkYellow"]=21
	colors["lightYellow"]=22
	colors["purple"]=30
	colors["lightPurple"]=9
	colors["darkPurple"]=8
	colors["black"]=1
	colors["white"]=16
	colors["brown"]=10
	colors["darkBrown"]=11
	colors["lightBrown"]=24
	colors["pink"]=20
	colors["orange"] =12

	#deal with axis, x is default
	if axis == "x":
		rot = (0, 0, 0)
	elif axis == "y":
		rot = (0, 0, 90)
	elif axis =="z":
		rot = (0, 90, 0)
	else:
		cmds.warning('createControl: you entered an incorrect axis. Must be x, y or z')

	#-------------------------do this from dictionary, that way it's easier to control the flow to error or return
	if type == "circle":
		cmds.circle(n=name, nr= (1,0,0))

	elif type == "cube":
		cmds.curve(n=name, d=1, p=[[-0.34095753069042323, -1.0031016006564133, 1.0031016006564133], [-0.34095753069042323, 1.0031016006564133, 1.0031016006564133], [0.34095753069042323, 1.0031016006564133, 1.0031016006564133], [0.34095753069042323, -1.0031016006564133, 1.0031016006564133], [-0.34095753069042323, -1.0031016006564133, 1.0031016006564133], [-0.34095753069042323, -1.0031016006564133, -1.0031016006564133], [-0.34095753069042323, 1.0031016006564133, -1.0031016006564133], [-0.34095753069042323, 1.0031016006564133, 1.0031016006564133], [0.34095753069042323, 1.0031016006564133, 1.0031016006564133], [0.34095753069042323, 1.0031016006564133, -1.0031016006564133], [0.34095753069042323, -1.0031016006564133, -1.0031016006564133], [0.34095753069042323, -1.0031016006564133, 1.0031016006564133], [0.34095753069042323, 1.0031016006564133, 1.0031016006564133], [0.34095753069042323, 1.0031016006564133, -1.0031016006564133], [-0.34095753069042323, 1.0031016006564133, -1.0031016006564133], [-0.34095753069042323, -1.0031016006564133, -1.0031016006564133], [0.34095753069042323, -1.0031016006564133, -1.0031016006564133]])

	elif type == "octagon":
		cmds.curve(n=name, d=1, p=[[-7.4559598726027055e-17, 0.70710670948028576, 0.70710670948028564], [5.5511098291698525e-17, 0.99999988079071067, 0.0], [-7.4559598726027055e-17, 0.70710670948028576, -0.70710670948028564], [-3.8857805861880489e-16, 1.7256332301709633e-31, -0.99999988079071045], [-7.0259651851158272e-16, -0.70710670948028576, -0.70710670948028564], [-8.326672684688675e-16, -1.0000000000000002, 0.0], [-7.0259654498136232e-16, -0.70710676908493053, 0.70710676908493042], [-3.8857805861880489e-16, 1.7256332301709633e-31, 0.99999994039535522], [-7.4559598726027055e-17, 0.70710670948028576, 0.70710670948028564]])

	elif type == "barbell":
		cmds.curve(n=name, d=3, p=[[0.57752510285324732, 5.5507632834890673e-17, -0.90650843775588597], [-2.9672778948456972e-16, 6.4094693518606145e-17, -1.661011590594498], [-0.57752510285324554, 5.550763283489071e-17, -0.90650843775588663], [-0.29814028408909887, 1.0540006765710255e-17, -0.67397322551417882], [-0.14033645814277884, -1.3393164286098273e-33, -2.7549060854235934e-16], [-0.29814028408909921, -1.0540006765710255e-17, 0.67397322551417838], [-0.57752510285324621, -5.5507632834890697e-17, 0.90650843775588641], [-6.6071759651022318e-16, -6.4094693518606133e-17, 1.6610115905944978], [0.57752510285324488, -5.550763283489074e-17, 0.90650843775588708], [0.29814028408909876, -1.0540006765710279e-17, 0.67397322551417937], [0.14033645814277884, -2.8148100723370156e-32, 8.7651446050535732e-16], [0.29814028408909921, 1.0540006765710236e-17, -0.6739732255141776]])
		cmds.closeCurve(name, ch=False, ps=False, rpo=True, bki=True)

	elif type == "sphere":
		cmds.curve(n=name, d=1, p=[[0.0, 1.0, 0.0], [-0.382683, 0.92388000000000003, 0.0], [-0.70710700000000004, 0.70710700000000004, 0.0], [-0.92388000000000003, 0.382683, 0.0], [-1.0, 0.0, 0.0], [-0.92388000000000003, -0.382683, 0.0], [-0.70710700000000004, -0.70710700000000004, 0.0], [-0.382683, -0.92388000000000003, 0.0], [0.0, -1.0, 0.0], [0.382683, -0.92388000000000003, 0.0], [0.70710700000000004, -0.70710700000000004, 0.0], [0.92388000000000003, -0.382683, 0.0], [1.0, 0.0, 0.0], [0.92388000000000003, 0.382683, 0.0], [0.70710700000000004, 0.70710700000000004, 0.0], [0.382683, 0.92388000000000003, 0.0], [0.0, 1.0, 0.0], [0.0, 0.92388000000000003, 0.382683], [0.0, 0.70710700000000004, 0.70710700000000004], [0.0, 0.382683, 0.92388000000000003], [0.0, 0.0, 1.0], [0.0, -0.382683, 0.92388000000000003], [0.0, -0.70710700000000004, 0.70710700000000004], [0.0, -0.92388000000000003, 0.382683], [0.0, -1.0, 0.0], [0.0, -0.92388000000000003, -0.382683], [0.0, -0.70710700000000004, -0.70710700000000004], [0.0, -0.382683, -0.92388000000000003], [0.0, 0.0, -1.0], [0.0, 0.382683, -0.92388000000000003], [0.0, 0.70710700000000004, -0.70710700000000004], [0.0, 0.92388000000000003, -0.382683], [0.0, 1.0, 0.0], [-0.382683, 0.92388000000000003, 0.0], [-0.70710700000000004, 0.70710700000000004, 0.0], [-0.92388000000000003, 0.382683, 0.0], [-1.0, 0.0, 0.0], [-0.92388000000000003, 0.0, 0.382683], [-0.70710700000000004, 0.0, 0.70710700000000004], [-0.382683, 0.0, 0.92388000000000003], [0.0, 0.0, 1.0], [0.382683, 0.0, 0.92388000000000003], [0.70710700000000004, 0.0, 0.70710700000000004], [0.92388000000000003, 0.0, 0.382683], [1.0, 0.0, 0.0], [0.92388000000000003, 0.0, -0.382683], [0.70710700000000004, 0.0, -0.70710700000000004], [0.382683, 0.0, -0.92388000000000003], [0.0, 0.0, -1.0], [-0.382683, 0.0, -0.92388000000000003], [-0.70710700000000004, 0.0, -0.70710700000000004], [-0.92388000000000003, 0.0, -0.382683], [-1.0, 0.0, 0.0]])


	elif type=="diamond":
		cmds.curve(n=name, d=1, p=[[3.1401849173675503e-16, 0.70710678118654768, 1.1102230246251565e-16], [4.9303806576313238e-32, 1.1102230246251568e-16, -0.70710678118654757], [-3.1401849173675503e-16, -0.70710678118654768, -1.1102230246251565e-16], [-4.9303806576313238e-32, -1.1102230246251568e-16, 0.70710678118654757], [3.1401849173675503e-16, 0.70710678118654768, 1.1102230246251565e-16]])

	else:
		cmds.warning("createControl doesn't know shape - '%s'"%type)

	#rotate to axis
	cmds.select(name+".cv[*]")
	cmds.rotate(rot[0], rot[1], rot[2], r=True)
	cmds.select(cl=True)
	shapes = cmds.listRelatives(name, shapes=True)
	for shape in shapes:
		cmds.setAttr("%s.overrideEnabled"%shape, 1)
		cmds.setAttr("%s.overrideColor"%shape, colors[color])
	#return the name of the curve
	return(name)

def createMessage(host="none", attr="none", target="none", *args):
	"""creates a message attr on object with target as value. Args are: 'host'-some object to hold the message attr, 'attr'-the name of the message attribute to create, and 'target'-the host to be the value of the message attr"""
	cmds.addAttr(host, at='message', ln=attr)
	cmds.connectAttr("%s.message"%target, "%s.%s"%(host, attr))
	return("%s.%s"%(host, attr))

def alignToUV(targetObj="none", sourceObj="none", sourceU=0.0, sourceV=0.0, mainAxis="+z", secAxis="+x", UorV="v"):
	"""
	inputs should be 1. targetObj 2. sourceObj 3. sourceU 4. sourceV 5. mainAxis(lowerCase, + or -, i.e."-x" 8. secAxis (lowcase, + or -) 7, UorV ("u" or "v" for the direction along surface for the sec axis)
"""

	axisDict = {"+x":(1,0,0), "+y":(0,1,0), "+z":(0,0,1), "-x":(-1,0,0), "-y":(0,-1,0), "-z":(0,0,-1)}

	#Does this create a new node? no To create a node, use the flag "ch=True". That creates a pointOnSurface node
	pos = cmds.pointOnSurface(sourceObj, u=sourceU, v=sourceV, position=True)
	posVec = om.MVector(pos[0], pos[1], pos[2])
	cmds.xform(targetObj, ws=True, t=pos)

	#get normal, tanU and tanV at selected UV position on source surface
	tanV = cmds.pointOnSurface(sourceObj, u=sourceU, v=sourceV, tv=True)
	tanU = cmds.pointOnSurface(sourceObj, u=sourceU, v=sourceV, tu=True)
	norm = cmds.pointOnSurface(sourceObj, u=sourceU, v=sourceV, nn=True)

	#decide where up axis is on normal constraint, u or v tangent
	if UorV == "v":
		wup = tanV
	elif UorV == "u":
		wup = tanU

	#create normal constraint
	nc = cmds.normalConstraint(sourceObj, targetObj, aimVector=axisDict[mainAxis], upVector=axisDict[secAxis], worldUpVector=(wup))
	cmds.delete(nc) #delete constraint

def groupOrient(target='none',orig='none', group="GRP"):
	"""
	groups the second object and snaps the group to the second (point and orient). The group arg is to name the suffix you want the group to have (default is '_GRP')
	Arguments: target (to be constrained to), orig (obj to move), group (suffix for group)
	"""
	if (target == "none"):
		sel = getTwoSelection()
		target = sel[0]
		orig = sel[1]

	cmds.select(orig)
	grpName = "%s_%s"%(orig,group)
	cmds.group(name=grpName)
	pc = cmds.pointConstraint(target, grpName)
	oc = cmds.orientConstraint(target, grpName)
	cmds.delete(pc)
	cmds.delete(oc)
	cmds.select(clear=True)

def stripToRotate(first="none", *args):
	attrs = ["tx", "ty", "tz", "sx", "sy", "sz", "visibility"]
	objs = []
	if first=="none":
		objs = getSelection()
	else:
		objs.append(first)
		if args:
			for each in args:
				objs.append(each)
##    print(objs)
	for me in objs:
		for attr in attrs:
			objAttr = me + "." + attr
			cmds.setAttr(objAttr, lock=True, k=False)

def stripToTranslate(first="none", *args):
	"""strips for all selected or entered as args, sets all attrs but translate to locked and hidden"""
	attrs = ["rx", "ry", "rz", "sx", "sy", "sz", "visibility"]
	objs = []
	if first=="none":
		objs = getSelection()
	else:
		objs.append(first)
		if args:
			for each in args:
				objs.append(each)
##    print(objs)
	for me in objs:
		for attr in attrs:
			objAttr = me + "." + attr
			cmds.setAttr(objAttr, lock=True, k=False)

def stripToRotateTranslate(first="none", *args):
	"""strips for all selected or entered as args, sets all attrs but translate to locked and hidden"""
	attrs = ["sx", "sy", "sz", "visibility"]
	objs = []
	if first=="none":
		objs = getSelection()
	else:
		objs.append(first)
		if args:
			for each in args:
				objs.append(each)
##    print(objs)
	for me in objs:
		for attr in attrs:
			objAttr = me + "." + attr
			cmds.setAttr(objAttr, lock=True, k=False)

def lockTranslate(first="none", *args):
	attrs = ["tx", "ty", "tz"]
	objs = []
	if first=="none":
		objs = getSelection()
	else:
		objs.append(first)
		if args:
			for each in args:
				objs.append(each)
	for me in objs:
		for attr in attrs:
			objAttr = me + "." + attr
			cmds.setAttr(objAttr, lock=True)

def stripTransforms(first="none", *args):
	"""locks and hides all transforms from channel box. can call multiple objs as arguments or use selection of objects"""
	attrs = ["rx", "ry", "rz", "tx", "ty", "tz", "sx", "sy", "sz", "visibility"]
	objs = []
	if first=="none":
		objs = getSelection()
	else:
		objs.append(first)
		if args:
			for each in args:
				objs.append(each)
	print(objs)
	for me in objs:
		for attr in attrs:
			objAttr = me + "." + attr
			cmds.setAttr(objAttr, lock=True, k=False)

def restoreTransforms(first="none", *args):
	"""restores all the default locked and hidden channels back to the channels box"""
	attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "visibility"]
	objs = []
	if first=="none":
		objs = getSelection()
	else:
		objs.append(first)
		for each in args:
			objs.append(each)
	print(objs)
	for me in objs:
		for attr in attrs:
			objAttr = me + "." + attr
			cmds.setAttr(objAttr, lock=False, k=True)

def createAdd(name, input1, input2):
	"""creates an addDoubleLinear node with name, object.attr, object.attr as args"""
	adl = cmds.shadingNode("addDoubleLinear", asUtility=True, name=name)
	cmds.connectAttr(input1, "%s.input1"%adl)
	cmds.connectAttr(input2, "%s.input2"%adl)
	return(adl)

def blendRotation(blend="none", sourceA="none", sourceB="none", target="none", sourceValue="none"):
	#add input and *args?
	"""name is first arg, then three objects. Blends rotation from first two selected into third selected. SourceValue (last input) is for the driving obj.attr. First source is active at '1', second at '2'"""
	if blend == "none":
		blend = "blendColors"
	if sourceA == "none":
		sel = getSelection()
		if len(sel) != 3:
			cmds.error("Error: blendRotation, select three transforms")
			#inert some kind of break here
		sourceA = sel[0]
		sourceB = sel[1]
		target = sel[2]
	blend = cmds.shadingNode("blendColors", asUtility=True, name=blend)
	sourceAOut = sourceA + ".rotate"
	sourceBOut = sourceB + ".rotate"
	targetIn = target + ".rotate"
	blend1 = blend + ".color1"
	blend2 = blend + ".color2"
	blendOut = blend + ".output"
	cmds.connectAttr(sourceAOut, blend1)
	cmds.connectAttr(sourceBOut, blend2)
	cmds.connectAttr(blendOut, targetIn)
	if not sourceValue == "none":
		cmds.connectAttr(sourceValue, "%s.blender"%blend)

	return(blend)

def blendTranslate(blend="none", sourceA="none", sourceB="none", target="none", sourceValue="none"):
	"""name is first arg, then three objects. Blends translation from first two selected into third selected. SourceValue (last input) is for the driving obj.attr. First source is active at '1', second at '2'"""
	#add input and *args
	if blend == "none":
		blend = "blendColors"
	if sourceA == "none":
		sel = getSelection()
		if len(sel) != 3:
			cmds.error("Error: blendRotation, select three transforms")
			#inert some kind of break here
		sourceA = sel[0]
		sourceB = sel[1]
		target = sel[2]
	blend = cmds.shadingNode("blendColors", asUtility=True, name=blend)
	sourceAOut = sourceA + ".translate"
	sourceBOut = sourceB + ".translate"
	targetIn = target + ".translate"
	blend1 = blend + ".color1"
	blend2 = blend + ".color2"
	blendOut = blend + ".output"
	cmds.connectAttr(sourceAOut, blend1)
	cmds.connectAttr(sourceBOut, blend2)
	cmds.connectAttr(blendOut, targetIn)
	if not sourceValue == "none":
		cmds.connectAttr(sourceValue, "%s.blender"%blend)

	return(blend)

def blendScale(blend="none", sourceA="none", sourceB="none", target="none", sourceValue="none"):
	"""name is first arg, then three objects. Blends translation from first two selected into third selected. SourceValue (last input) is for the driving obj.attr. First source is active at '1', second at '2'"""
	#add input and *args
	if blend == "none":
		blend = "blendColors"
	if sourceA == "none":
		sel = getSelection()
		if len(sel) != 3:
			cmds.error("Error: blendRotation, select three transforms")
			#inert some kind of break here
		sourceA = sel[0]
		sourceB = sel[1]
		target = sel[2]
	blend = cmds.shadingNode("blendColors", asUtility=True, name=blend)
	sourceAOut = sourceA + ".scale"
	sourceBOut = sourceB + ".scale"
	targetIn = target + ".scale"
	blend1 = blend + ".color1"
	blend2 = blend + ".color2"
	blendOut = blend + ".output"
	cmds.connectAttr(sourceAOut, blend1)
	cmds.connectAttr(sourceBOut, blend2)
	cmds.connectAttr(blendOut, targetIn)
	if not sourceValue == "none":
		cmds.connectAttr(sourceValue, "%s.blender"%blend)

	return(blend)


# def colorControl(color="none", *args):
# 	"""enter a color (red, blue, green, yellow, dkRed, dkBlue, dkGreen, dkYellow, pink, ltBlue, ltGreen, ltYellow, black, purple), then objs or selection"""
# 	if color == "none":
# 		cmds.error("must choose a color to use 'colorControl'")
# 	#create dictionary
# 	colors = {"red":13}
# 	if args == ():
# 		args = getSelection()
# 	for obj in args:
# 		#get shape node
# 		#check to make sure there is a shape node
# 		#set coloroverride to 1
# 		#set color to color value of dict
# 		pass


# def standInGeo():
# ##  check that there is a next joint
# ##  measure distance to next joint?
# ##	create geo that is scaled to that measurement
# ##	snap the geo to the joint
# 	pass

def addGroupAbove(obj="none", suff="none", *args):
	"""name of existing obj, new group suffix. New group will be oriented to the object BELOW it"""
	#FIX THE OBJ, SUFIX TO BE EITHER SELECTED OR ENTERED
	sel = cmds.ls(sl=True, type = "transform")
	for obj in sel:
		suff = "_new"
		name = obj + suff + "_GRP"
		#get worldspace location of existing obj
		loc = cmds.xform(obj, q=True, ws=True, rp=True)
		#create new group, name it, move it to new postion in ws and Orient it
		grp = cmds.group(empty=True, name=name)
		cmds.move(loc[0], loc[1], loc[2], grp, ws=True)
		oc = cmds.orientConstraint(obj, grp)
		cmds.delete(oc)
		#check if there's a parent to the old group
		par = cmds.listRelatives(obj, p=True)
		print(par)
		if par:
			cmds.parent(grp, par)
		cmds.parent(obj, grp)

def reverseSetup(inAttr, strAttr, revAttr, rName, *args):
	"""
	4 arguments, the (node.attr) that enters the rev, straight conn,
	the reversed, then the reverse node name
	"""
	cmds.shadingNode("reverse", asUtility=True, name=rName)
	rIn = rName + ".input"
	rOut = rName + ".output"
	cmds.connectAttr(inAttr, strAttr)
	cmds.connectAttr(inAttr, rIn)
	cmds.connectAttr(rOut, revAttr)
	cmds.select(cl=True)

# def addExpression():
# ##    expr = "code goes here"
# ##    obj = []
# ##    cmds.expression(object=obj, string=expr)
# 	pass

# def snapToVertex():
# ##    get the selection of vertex (flatten it?)
# ##    get the worldspace location of the vertex
# ##    move the obj to the location of the vertex
# 	pass

# def nameTypeSelection():
# ##    get wildcard selection and type selection
# ##    loop selection to select add
# 	pass

# def createQSS(name="none", *args):
# ##    if name == "none":
# ##        cmds.error("you must enter a name and a selection (either manual or as arguments")
# ##    else:
# ##        for arg in args:

# ##    get the objects (*args)
# ##    create QSS using either selection or *args
# 	pass

def measureDistance(mName="none", *args):
	"""first the name of the measure node, then the 2 objects ORRRR select the two objects and run (will give name 'distanceBetween'"""
	objs = []
	if mName == "none":
		mName = "distanceBetween"
		objs = getTwoSelection()
	else:
		for each in args:
			objs.append(each)
	#add check for 2 selectiont
	if len(objs) != 2:
		cmds.error("you must enter either a measure name and 2 objects OR no arguments and manually select 2 objs")
	dist = cmds.shadingNode("distanceBetween", asUtility=True, name=mName)
	objA = objs[0]
	objB = objs[1]
	objAMatrix = objA + ".worldMatrix"
	objBMatrix = objB + ".worldMatrix"
	objAPoint = objA + ".rotatePivot"
	objBPoint = objB + ".rotatePivot"
	distPoint1 = dist + ".point1"
	distPoint2 = dist + ".point2"
	distMatrix1 = dist + ".inMatrix1"
	distMatrix2 = dist + ".inMatrix2"
	cmds.connectAttr(objAPoint, distPoint1)
	cmds.connectAttr(objBPoint, distPoint2)
	cmds.connectAttr(objAMatrix, distMatrix1)
	cmds.connectAttr(objBMatrix, distMatrix2)
	cmds.select(clear=True)
	return(dist)

def scaleStretchIK(limbName="none", ikTop="none", ikMid="none", ikLow="none", jntMeasure="none", IKMeasure="none", IKCtrl="none", axis="none", *args):
	"""creates a stretch setup for 3 joint IK chain. Inputs (strings) are the limbName, 3 ik joints (top to bottom), the measure input for the whole chain (add up from measure joints), the measure for the ikCtrl, the ik handle or ctrl (which must have 'scaleMin', 'upScale' and 'lowScale' attrs, the axis letter. Returns . . . """

	ratioMult = cmds.shadingNode("multiplyDivide", asUtility=True, n="%s_stretchRatioMult"%limbName)
	cmds.setAttr(ratioMult + ".operation", 2)
	cmds.connectAttr(jntMeasure, "%s.input2X"%ratioMult)
	cmds.connectAttr(IKMeasure, "%s.input1X"%ratioMult)

	#could put this default stuff (next two paragraphs) after the conditional and use another conditional so that minScale is bundled up in "autostretch"
	#create default setting of 1 when autostretch is off
	defaultMult = cmds.shadingNode("multiplyDivide", asUtility=True, n="%s_stretchDefaultMult"%limbName)
	cmds.setAttr("%s.input1X"%defaultMult, 1)

	#create blend node to blend ratio mult and default values, based on blender attr of ikctrl.autoStretch
	defaultBlend = cmds.shadingNode("blendColors", asUtility=True, n="%s_stretchBlend"%limbName)
	cmds.connectAttr("%s.outputX"%defaultMult, "%s.color2R"%defaultBlend)
	cmds.connectAttr("%s.outputX"%ratioMult, "%s.color1R"%defaultBlend)
	cmds.connectAttr("%s.autoStretch"%IKCtrl, "%s.blender"%defaultBlend)

	#blend goes into condition node - firstTerm, secondTerm=ikctrl scaleMin value, operation=2(greaterthan), colorIfTrue is blend, colorIfFalse is scaleMin attr
	conditional = cmds.shadingNode("condition", asUtility=True, n="%s_upStretchCondition"%limbName)
	cmds.setAttr("%s.operation"%conditional, 2)
	cmds.connectAttr("%s.outputR"%defaultBlend, "%s.firstTerm"%conditional)
	cmds.connectAttr("%s.scaleMin"%IKCtrl, "%s.secondTerm"%conditional)
	cmds.connectAttr("%s.outputR"%defaultBlend, "%s.colorIfTrueR"%conditional)
	cmds.connectAttr("%s.scaleMin"%IKCtrl, "%s.colorIfFalseR"%conditional)

	#factor in the upScale/lowScale attrs
	upScaleMult = cmds.shadingNode('multiplyDivide', asUtility=True, n="%s_upScaleMult"%limbName)
	cmds.connectAttr("%s.outColorR"%conditional, "%s.input1X"%upScaleMult)
	cmds.connectAttr("%s.upScale"%IKCtrl, "%s.input2X"%upScaleMult)
	loScaleMult = cmds.shadingNode('multiplyDivide', asUtility=True, n="%s_loScaleMult"%limbName)
	cmds.connectAttr("%s.outColorR"%conditional, "%s.input1X"%loScaleMult)
	cmds.connectAttr("%s.lowScale"%IKCtrl, "%s.input2X"%loScaleMult)

	#hook up the scales of the joints
	cmds.connectAttr("%s.outputX"%upScaleMult, "%s.s%s"%(ikTop, axis))
	cmds.connectAttr("%s.outputX"%loScaleMult, "%s.s%s"%(ikMid, axis))

	return(ratioMult, defaultMult, defaultBlend, conditional, upScaleMult, loScaleMult)

def translateStretchIK(limbName="none", ikTop="none", ikMid="none", ikLow="none", jntMeasure="none", IKMeasure="none", IKCtrl="none", axis="none", posNeg="none", *args):
	"""creates a stretch setup for 3 joint IK chain. Inputs (strings) are the limbName, 3 ik joints (top to bottom), the measure input for the whole chain (add up from measure joints?), the measure for the ikCtrl, the ik handle or ctrl (which must have 'scaleMin' attr, the axis letter, and PosNeg, which is +1 or -1 (minus for things in negative direction/mirror). Returns . . . """
	#set up the ratio of ctrl to measure
	ratioMult = cmds.shadingNode("multiplyDivide", asUtility=True, n="%s_stretchRatioMult"%limbName)
	cmds.setAttr(ratioMult + ".operation", 2)
	cmds.connectAttr(jntMeasure, "%s.input2X"%ratioMult)
	cmds.connectAttr(IKMeasure, "%s.input1X"%ratioMult)

	#create default setting of 1 when autostretch is off
	default = cmds.shadingNode("multiplyDivide", asUtility=True, n="%s_stretchDefaultMult"%limbName)
	cmds.setAttr("%s.input1X"%default, 1)

	#create blend node to blend ratio mult and default values, based on blender attr of ikctrl.autoStretch
	defaultBlend = cmds.shadingNode("blendColors", asUtility=True, n="%s_stretchBlend")
	cmds.connectAttr("%s.outputX"%default, "%s.color2R"%defaultBlend)
	cmds.connectAttr("%s.outputX"%ratioMult, "%s.color1R"%defaultBlend)
	cmds.connectAttr("%s.autoStretch"%IKCtrl, "%s.blender"%defaultBlend)

	#get the top joint length
	tAxis = "t%s"%axis
	topLength = cmds.getAttr("%s.%s"%(ikMid, tAxis))
	#do I need measure joints?

	#create length factor for top
	topFactorMult = cmds.shadingNode("multiplyDivide", asUtility=True, n="%s_stretchFactorTopMult"%limbName)
	cmds.setAttr("%s.input1X"%topFactorMult, topLength)
	cmds.connectAttr("%s.outputR"%defaultBlend,"%s.input2X"%topFactorMult)

	#set up for clamp
	topClamp = cmds.shadingNode("clamp", asUtility=True, n="%s_stretchTopClamp"%limbName)
	cmds.connectAttr("%s.outputX"%topFactorMult, "%s.inputR"%topClamp)

	#create min, max, connect to clamp
	topMin = cmds.shadingNode("multiplyDivide", asUtility=True, n="%s_topMinMult"%limbName)
	topMax = cmds.shadingNode("multiplyDivide", asUtility=True, n="%s_topMaxMult"%limbName)
	if posNeg == 1:
		cmds.setAttr("%s.input1X"%topMin, topLength)
		cmds.connectAttr("%s.scaleMin"%IKCtrl, "%s.input2X"%topMin)
		cmds.setAttr("%s.input1X"%topMax, topLength)
		cmds.setAttr("%s.input2X"%topMax, 4)
		cmds.connectAttr("%s.outputX"%topMin, "%s.minR"%topClamp)
		cmds.connectAttr("%s.outputX"%topMax, "%s.maxR"%topClamp)
	if posNeg == -1:
		cmds.setAttr("%s.input1X"%topMax, topLength)
		cmds.connectAttr("%s.scaleMin"%IKCtrl, "%s.input2X"%topMax)
		cmds.setAttr("%s.input1X"%topMin, topLength)
		cmds.setAttr("%s.input2X"%topMin, 4)
		cmds.connectAttr("%s.outputX"%topMin, "%s.minR"%topClamp)
		cmds.connectAttr("%s.outputX"%topMax, "%s.maxR"%topClamp)

	#connect to joints
	cmds.connectAttr("%s.outputR"%topClamp, "%s.%s"%(ikMid, tAxis))

	#do lower half
	#get the low joint length
	tAxis = "t%s"%axis
	lowLength = cmds.getAttr("%s.%s"%(ikLow, tAxis))
	#do I need measure joints?

	#create length factor for low
	lowFactorMult = cmds.shadingNode("multiplyDivide", asUtility=True, n="%s_stretchFactorLowMult"%limbName)
	cmds.setAttr("%s.input1X"%lowFactorMult, lowLength)
	cmds.connectAttr("%s.outputR"%defaultBlend,"%s.input2X"%lowFactorMult)

	#set up for clamp
	lowClamp = cmds.shadingNode("clamp", asUtility=True, n="%s_stretchlowClamp"%limbName)
	cmds.connectAttr("%s.outputX"%lowFactorMult, "%s.inputR"%lowClamp)

	#create min, max, connect to clamp
	lowMin = cmds.shadingNode("multiplyDivide", asUtility=True, n="%s_lowMinMult"%limbName)
	lowMax = cmds.shadingNode("multiplyDivide", asUtility=True, n="%s_lowMaxMult"%limbName)
	if posNeg == 1:
		cmds.setAttr("%s.input1X"%lowMin, lowLength)
		cmds.connectAttr("%s.scaleMin"%IKCtrl, "%s.input2X"%lowMin)
		cmds.setAttr("%s.input1X"%lowMax, (lowLength*posNeg))
		cmds.setAttr("%s.input2X"%lowMax, 4)
		cmds.connectAttr("%s.outputX"%lowMin, "%s.minR"%lowClamp)
		cmds.connectAttr("%s.outputX"%lowMax, "%s.maxR"%lowClamp)
	if posNeg == (-1):
		cmds.setAttr("%s.input1X"%lowMax, lowLength)
		cmds.connectAttr("%s.scaleMin"%IKCtrl, "%s.input2X"%lowMax)
		cmds.setAttr("%s.input1X"%lowMin, lowLength)
		cmds.setAttr("%s.input2X"%lowMin, 4)
		cmds.connectAttr("%s.outputX"%lowMin, "%s.minR"%lowClamp)
		cmds.connectAttr("%s.outputX"%lowMax, "%s.maxR"%lowClamp)
	#connect to joints
	cmds.connectAttr("%s.outputR"%lowClamp, "%s.%s"%(ikLow, tAxis))


	return(ratioMult, topFactorMult, lowFactorMult, topMin, topMax, lowMin, lowMax, topClamp, lowClamp)

# def curveInfo():
# 	pass

# def attachToCurve():
# 	pass

# def jointCleanUp():
# 	pass
##    OR select top joint, unparent child, zero rots, parent back (for multiple children)?
##    zero rotations
##    parent child back to parent
##    orientJoints

def makePlane(*args):
	points = []
	cmds.polyCreateFacetCtx(pc=False)
	sel = cmds.ls(sl=True, type="transform")
	for obj in sel:
		loc = cmds.pointPosition((obj + ".rotatePivot"), world=True)
		points.append(loc)
		poly = cmds.polyCreateFacet(p=points)
##    try to figure out if theyre planar or not, give warning?


#show/hide selected local rot axes

