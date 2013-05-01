import maya.cmds as cmds

#TO-DO----------------put the softmod under a follicle that is attached to the skin?
#TO-DO----------------add soft select to another tab, figure out control, etc.
#TO-DO----------------maybe option to orient to the vertex? Is that even possible w/ softmod
#TO-DO----------------see if I can get the softmod deformer itself to rotate? I could connect it to normal of closest point?

widgets = {}

def softModDeformerUI():
	if cmds.window("softModWin", exists = True):
		cmds.deleteUI("softModWin")
	widgets["window"] = cmds.window("softModWin", t="SoftMod Deformer", w=300, h=130)
	widgets["tabLO"] = cmds.tabLayout()
	widgets["columnLO"] = cmds.columnLayout("SoftModDeformer", w=300)

	cmds.separator(h=10)
	widgets["nameTFG"] = cmds.textFieldGrp(l="Deformer Name", w=300, cw=[(1,100),(2,190)], cal=[(1,"left"), (2, "left")], tx="softMod_DEF")
	widgets["firstVertCBG"] = cmds.checkBoxGrp(l="Use only 1st vert (vs. avg pos)", v1=0, cw=[(1,200)], cal=[(1,"left"), (2,"left")])
	widgets["parentCBG"] = cmds.checkBoxGrp(l="Parent Ctrl Under Geo?", v1=0, cw=[(1,200)], cal=[(1,"left"), (2,"left")])
	widgets["incrCBG"] = cmds.checkBoxGrp(l="Increment name after creation?", v1=1, cw=[(1,200)], cal=[(1,"left"), (2,"left")])
	widgets["checkCBG"] = cmds.checkBoxGrp(l="AutoCheck if there are deformers?", v1=1, cw=[(1,200)], cal=[(1,"left"), (2,"left")])
	widgets["scaleFFG"] = cmds.floatFieldGrp(l="Control Scale", v1=1, pre=2, cw=[(1,100),(2,50)], cal=[(1,"left"),(2,"left")])

	cmds.separator(h=10, style="single")
	widgets["button"] = cmds.button(l="Create Deformer", w=300, h=40, bgc=(.6,.8,.6), c=softModDeformerDo)

	cmds.showWindow(widgets["window"])

def softModDeformerDo(*args):
#TO-DO----------------use long names for objects?
	check = cmds.checkBoxGrp(widgets["checkCBG"], q=True, v1=True)
	increment = cmds.checkBoxGrp(widgets["incrCBG"], q=True, v1=True)
	toParent = cmds.checkBoxGrp(widgets["parentCBG"], q=True, v1=True)
	#get deformer name
	defName = cmds.textFieldGrp(widgets["nameTFG"], tx=True, q=True)

	if not (cmds.objExists(defName)):
		# choose a vert (for example)
		vertsRaw = cmds.ls(sl=True, fl=True)

		if vertsRaw == []:
			cmds.warning("Must select at least one vertex")
		else:
			if (cmds.checkBoxGrp(widgets["firstVertCBG"], q=True, v1=True)):
				vertex = [vertsRaw[0]]
			else:
				vertex = vertsRaw

		obj = vertex[0].partition(".")[0]

		#get vert position then select the geo
		positions = []
		for vert in vertex:
			positions.append(cmds.pointPosition(vert))

		numVerts = len(positions)

		x,y,z = 0,0,0
		for i in range(numVerts):
			x += positions[i][0]
			y += positions[i][1]
			z += positions[i][2]

		vertPos = [(x/numVerts), (y/numVerts), (z/numVerts)]

		#check if there are other deformers on the obj
		if check:
			deformers = []
			deformers = getDeformers(obj)
			if deformers:
				cmds.confirmDialog( title='Deformer Alert!', message='Found some deformers on %s.\nYou may want to put the softmod\n early in the input list'%obj, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )

		cmds.select(obj)

		# create a soft mod at vert position (avg)
		softMod = defName
		softModOrig = cmds.softMod(relative=False, falloffCenter = vertPos, falloffRadius=5.0, n=softMod)[0]
		cmds.rename(softModOrig, softMod)
		softModXform = cmds.listConnections(softModOrig, type="transform")[0]


		# create a control at the position of the softmod
		control = defName + "_CTRL"
		cmds.curve(n=control, d=1, p=[[0.0, 1.0, 0.0], [-0.382683, 0.92388000000000003, 0.0], [-0.70710700000000004, 0.70710700000000004, 0.0], [-0.92388000000000003, 0.382683, 0.0], [-1.0, 0.0, 0.0], [-0.92388000000000003, -0.382683, 0.0], [-0.70710700000000004, -0.70710700000000004, 0.0], [-0.382683, -0.92388000000000003, 0.0], [0.0, -1.0, 0.0], [0.382683, -0.92388000000000003, 0.0], [0.70710700000000004, -0.70710700000000004, 0.0], [0.92388000000000003, -0.382683, 0.0], [1.0, 0.0, 0.0], [0.92388000000000003, 0.382683, 0.0], [0.70710700000000004, 0.70710700000000004, 0.0], [0.382683, 0.92388000000000003, 0.0], [0.0, 1.0, 0.0], [0.0, 0.92388000000000003, 0.382683], [0.0, 0.70710700000000004, 0.70710700000000004], [0.0, 0.382683, 0.92388000000000003], [0.0, 0.0, 1.0], [0.0, -0.382683, 0.92388000000000003], [0.0, -0.70710700000000004, 0.70710700000000004], [0.0, -0.92388000000000003, 0.382683], [0.0, -1.0, 0.0], [0.0, -0.92388000000000003, -0.382683], [0.0, -0.70710700000000004, -0.70710700000000004], [0.0, -0.382683, -0.92388000000000003], [0.0, 0.0, -1.0], [0.0, 0.382683, -0.92388000000000003], [0.0, 0.70710700000000004, -0.70710700000000004], [0.0, 0.92388000000000003, -0.382683], [0.0, 1.0, 0.0], [-0.382683, 0.92388000000000003, 0.0], [-0.70710700000000004, 0.70710700000000004, 0.0], [-0.92388000000000003, 0.382683, 0.0], [-1.0, 0.0, 0.0], [-0.92388000000000003, 0.0, 0.382683], [-0.70710700000000004, 0.0, 0.70710700000000004], [-0.382683, 0.0, 0.92388000000000003], [0.0, 0.0, 1.0], [0.382683, 0.0, 0.92388000000000003], [0.70710700000000004, 0.0, 0.70710700000000004], [0.92388000000000003, 0.0, 0.382683], [1.0, 0.0, 0.0], [0.92388000000000003, 0.0, -0.382683], [0.70710700000000004, 0.0, -0.70710700000000004], [0.382683, 0.0, -0.92388000000000003], [0.0, 0.0, -1.0], [-0.382683, 0.0, -0.92388000000000003], [-0.70710700000000004, 0.0, -0.70710700000000004], [-0.92388000000000003, 0.0, -0.382683], [-1.0, 0.0, 0.0]])
	#TO-DO----------------scale the cv's based on the number from the UI
		cmds.select(cl=True)
	#TO-DO----------------pull this out into separate function?? Args would be object and color
		shapes = cmds.listRelatives(control, shapes=True)
		for shape in shapes:
		    cmds.setAttr("%s.overrideEnabled"%shape, 1)
		    cmds.setAttr("%s.overrideColor"%shape, 14)
		controlGrp = cmds.group(control, n="%s_GRP"%control)
		cmds.xform(controlGrp, ws=True, t=vertPos)

		# connect the pos, rot, scale of the control to the softModHandle
		cmds.connectAttr("%s.translate"%control, "%s.translate"%softModXform)
		cmds.connectAttr("%s.rotate"%control, "%s.rotate"%softModXform)
		cmds.connectAttr("%s.scale"%control, "%s.scale"%softModXform)

		# create an attr on the control for the falloff and the center control vis
		cmds.addAttr(control, ln="falloff", at="float", min=0, max=100, k=True, dv=5)
		cmds.addAttr(control, ln="centerCtrlVis", at="bool", min=0, max=1, k=True, dv=0)

		# connect that attr to the softmod falloff radius
		cmds.connectAttr("%s.falloff"%control, "%s.falloffRadius"%softMod)

		# inherit transforms on softModHandle are "off"
		cmds.setAttr("%s.inheritsTransform"%softModXform, 0)

	#TO-DO----------------add option to change softmod from volume to surface?
		centerName = defName + "_center_CTRL"
		#create secondary (area of influence) control here
		centerCtrl = cmds.curve(n=centerName, d=1, p=[[-1.137096, -1.137096, 1.137096], [-1.137096, 1.137096, 1.137096], [1.137096, 1.137096, 1.137096], [1.137096, -1.137096, 1.137096], [-1.137096, -1.137096, 1.137096], [-1.137096, -1.137096, -1.137096], [-1.137096, 1.137096, -1.137096], [-1.137096, 1.137096, 1.137096], [1.137096, 1.137096, 1.137096], [1.137096, 1.137096, -1.137096], [1.137096, -1.137096, -1.137096], [1.137096, -1.137096, 1.137096], [1.137096, -1.137096, -1.137096], [-1.137096, -1.137096, -1.137096], [-1.137096, 1.137096, -1.137096], [1.137096, 1.137096, -1.137096]])
	#TO-DO----------------scale the cv's based on the number from the UI
		centerCtrlSh = cmds.listRelatives(centerCtrl, s=True)
		for shape in centerCtrlSh:
			#turn on overrides
			cmds.setAttr("%s.overrideEnabled"%shape, 1)
			cmds.connectAttr("%s.centerCtrlVis"%control, "%s.overrideVisibility"%shape)
			cmds.setAttr("%s.overrideColor"%shape, 13)

		centerGrp = cmds.group(centerCtrl, n="%s_GRP"%centerName)
		#turn off scale and rotation for the center control
		cmds.setAttr("%s.rotate"%centerCtrl, k=False, l=True)
		cmds.setAttr("%s.scale"%centerCtrl, k=False, l=True)
		cmds.setAttr("%s.visibility"%centerCtrl, k=False, l=True)

		#move the group to the location
		cmds.xform(centerGrp, ws=True, t=vertPos)

		# create decompose matrix node and connect world matrix of centercontrol to falloffCenter
		decompName = defName + "_decomp"
		decomp = cmds.shadingNode("decomposeMatrix", asUtility=True, n=decompName)
		# connect centerCtrl to decompMatrix, connect decompMatrix.outputTranslate to falloffCenter
		cmds.connectAttr("%s.worldMatrix[0]"%centerCtrl, "%s.inputMatrix"%decomp)
		cmds.connectAttr("%s.outputTranslate"%decomp, "%s.falloffCenter"%softMod)

		#hide the softmod
		cmds.setAttr("%s.visibility"%softModXform, 0)

		#group the group and the softmod xform
		defGroup = cmds.group(softModXform, controlGrp, n=(defName + "_deform_GRP"))

		#parent the softmod under the centerCtrl
		cmds.parent(defGroup, centerCtrl)

		#parent that group under the obj?
		if toParent:
			cmds.parent(centerGrp, obj)

		#increment name
		if increment == 1:
			print "trying to rename"
			split = defName.rpartition("_")
			end = split[2]
			isInt = integerTest(end)

			if isInt:
				newNum = int(end) + 1
				newName = "%s%s%02d"%(split[0], split[1], newNum)
				cmds.textFieldGrp(widgets["nameTFG"], tx=newName, e=True)
			else:
				newName = "%s_01"%defName
				cmds.textFieldGrp(widgets["nameTFG"], tx=newName, e=True)

		#select the control to wrap up
		cmds.select(control)
	else:
		cmds.warning("An object of this name, %s, already exists! Choose a new name!"%defName)

def integerTest(test, *args):
	"""use to test if a variable is an integer"""
	try:
		int(test)
		return True
	except:
		return False

def getDeformers(obj, *args):
	history = cmds.listHistory(obj)
	Arrdeformers = []
	for node in history:
		types = cmds.nodeType(node, inherited = True)
		if "geometryFilter" in types:
			Arrdeformers.append(types[1])
	return Arrdeformers

def softModDeformer():
	softModDeformerUI()


