import maya.cmds as cmds

widgets = {}

def softModDeformerUI():
	if cmds.window("softModWin", exists = True):
		cmds.deleteUI("softModWin")
	widgets["window"] = cmds.window("softModWin", t="SoftMod Deformer", w=300, h=120)

	widgets["columnLO"] = cmds.columnLayout(w=300, h=120)
	cmds.separator(h=10)
	widgets["nameTFG"] = cmds.textFieldGrp(l="Deformer Name", w=300, cw=[(1,100),(2,190)], cal=[(1,"left"), (2, "left")])
	widgets["firstVertCBG"] = cmds.checkBoxGrp(l="Use only 1st vert (vs. avg pos)", v1=0, cw=[(1,200)], cal=[(1,"left"), (2,"left")])
	widgets["parentCBG"] = cmds.checkBoxGrp(l="Parent Ctrl Under Geo?", v1=1, cw=[(1,200)], cal=[(1,"left"), (2,"left")])
	#entry for scale size of controller?
	#entry for type of control? color of control?
	#text for instructions
	widgets["button"] = cmds.button(l="Create Deformer", w=300, h=50, c=softModDeformer)

	cmds.showWindow(widgets["window"])

def softModDeformer(*args):

	#get deformer name
	defName = cmds.textFieldGrp(widgets["nameTFG"], tx=True, q=True)

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

	cmds.select(obj)

	# create a soft mod at vert position (avg)
	softMod = defName
	softModOrig = cmds.softMod(relative=False, falloffCenter = vertPos, falloffRadius=5.0, n=softMod)[0]
	cmds.rename(softModOrig, softMod)
	softModXform = cmds.listConnections(softModOrig, type="transform")[0]


	# create a control at the position of the softmod
	control = defName + "_CTRL"
	cmds.curve(n=control, d=1, p=[[0.0, 1.0, 0.0], [-0.382683, 0.92388000000000003, 0.0], [-0.70710700000000004, 0.70710700000000004, 0.0], [-0.92388000000000003, 0.382683, 0.0], [-1.0, 0.0, 0.0], [-0.92388000000000003, -0.382683, 0.0], [-0.70710700000000004, -0.70710700000000004, 0.0], [-0.382683, -0.92388000000000003, 0.0], [0.0, -1.0, 0.0], [0.382683, -0.92388000000000003, 0.0], [0.70710700000000004, -0.70710700000000004, 0.0], [0.92388000000000003, -0.382683, 0.0], [1.0, 0.0, 0.0], [0.92388000000000003, 0.382683, 0.0], [0.70710700000000004, 0.70710700000000004, 0.0], [0.382683, 0.92388000000000003, 0.0], [0.0, 1.0, 0.0], [0.0, 0.92388000000000003, 0.382683], [0.0, 0.70710700000000004, 0.70710700000000004], [0.0, 0.382683, 0.92388000000000003], [0.0, 0.0, 1.0], [0.0, -0.382683, 0.92388000000000003], [0.0, -0.70710700000000004, 0.70710700000000004], [0.0, -0.92388000000000003, 0.382683], [0.0, -1.0, 0.0], [0.0, -0.92388000000000003, -0.382683], [0.0, -0.70710700000000004, -0.70710700000000004], [0.0, -0.382683, -0.92388000000000003], [0.0, 0.0, -1.0], [0.0, 0.382683, -0.92388000000000003], [0.0, 0.70710700000000004, -0.70710700000000004], [0.0, 0.92388000000000003, -0.382683], [0.0, 1.0, 0.0], [-0.382683, 0.92388000000000003, 0.0], [-0.70710700000000004, 0.70710700000000004, 0.0], [-0.92388000000000003, 0.382683, 0.0], [-1.0, 0.0, 0.0], [-0.92388000000000003, 0.0, 0.382683], [-0.70710700000000004, 0.0, 0.70710700000000004], [-0.382683, 0.0, 0.92388000000000003], [0.0, 0.0, 1.0], [0.382683, 0.0, 0.92388000000000003], [0.70710700000000004, 0.0, 0.70710700000000004], [0.92388000000000003, 0.0, 0.382683], [1.0, 0.0, 0.0], [0.92388000000000003, 0.0, -0.382683], [0.70710700000000004, 0.0, -0.70710700000000004], [0.382683, 0.0, -0.92388000000000003], [0.0, 0.0, -1.0], [-0.382683, 0.0, -0.92388000000000003], [-0.70710700000000004, 0.0, -0.70710700000000004], [-0.92388000000000003, 0.0, -0.382683], [-1.0, 0.0, 0.0]])
	cmds.select(cl=True)
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

	# create an attr on the control for the falloff (and the envelope)
	cmds.addAttr(control, ln="falloff", at="float", min=0, max=100, k=True, dv=5)

	# connect that attr to the softmod falloff radius
	cmds.connectAttr("%s.falloff"%control, "%s.falloffRadius"%softMod)

	# inherit transforms on softModHandle are "off"
	cmds.setAttr("%s.inheritsTransform"%softModXform, 0)

#TO-DO----------------
	# create secondary control under control
	# this will drive falloff center attr of the softmod (connect attrs from translate)

	#hide the softmod
	cmds.setAttr("%s.visibility"%softModXform, 0)

	#group the group and the softmod xform
	defGroup = cmds.group(softModXform, controlGrp, n=(defName + "_deform_GRP"))

	#parent that group under the obj?
	cmds.parent(defGroup, obj)

	#select the control to wrap up
	cmds.select(control)

def zbw_softModDeformer():
	softModDeformerUI()


