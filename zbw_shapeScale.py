########################
#file: zbw_shapeScale.py
#author: zeth willie
#contact: zeth@catbuks.com, www.williework.blogspot.com, https://github.com/zethwillie
#date modified: 09/23/12
#
#notes: creates a uI that one can use to scale selected nurbs curves from the cvs
########################


import maya.cmds as cmds

widgets = {}

def shapeScaleUI():
	if (cmds.window("ssWin", exists=True)):
		cmds.deleteUI("ssWin", window=True)
		#cmds.winPref("shapeScaleWin", remove=True)

	widgets["win"] = cmds.window("ssWin", t="zbw_shapeScale", w=400, h=110)

#TO-DO----------------form layout, section on right is the record scale section
	widgets["colLo"] = cmds.columnLayout("mainCLO", w=400, h=110)
	widgets["formLO"] = cmds.formLayout(nd=100, w=400)
	cmds.separator(h=10)
	widgets["slider"] = cmds.floatSliderGrp("slider", f=False, l="Scale", min=0.01, max=2, pre=3, v=1, adj=3, cal=([1, "left"], [2, "left"], [3, "left"]), cw=([1, 50], [2,220]), cc= shapeScaleExecute)
	cmds.separator(h=10)
	widgets["scaleFFG"] = cmds.floatFieldGrp(v1=100, pre= 1, l="Scale %", en1=True, w=110, cw=([1,50],[2,50]), cal=([1,"left"], [2,"left"]))
	widgets["scaleDoBut"] = cmds.button(l="Scale", w= 160, c=manualScale)
	# widgets["recBut"] = cmds.button(l="REC", w=40)
	widgets["clearBut"] = cmds.button(l="RESET", w=100)
	widgets["trackerFFG"] = cmds.floatFieldGrp(l="Change", w=100, v1=100, pre=1, en1=False, cw=([1,40],[2,50]), cal=([1,"left"], [2,"left"]), bgc=(0,0,0))

	#attach to form layout
	cmds.formLayout(widgets["formLO"], e=True, attachForm=[(widgets["slider"], 'top', 5), (widgets["slider"], 'left', 5)])
	cmds.formLayout(widgets["formLO"], e=True, attachForm=[(widgets["scaleFFG"], 'top', 30), (widgets["scaleFFG"], 'left', 5)])
	cmds.formLayout(widgets["formLO"], e=True, attachForm=[(widgets["scaleDoBut"], 'top', 30), (widgets["scaleDoBut"], 'left', 120)])
	# cmds.formLayout(widgets["formLO"], e=True, attachForm=[(widgets["recBut"], 'top', 30), (widgets["recBut"], 'left', 300)])
	cmds.formLayout(widgets["formLO"], e=True, attachForm=[(widgets["clearBut"], 'top', 30), (widgets["clearBut"], 'left', 300)])
	cmds.formLayout(widgets["formLO"], e=True, attachForm=[(widgets["trackerFFG"], 'top', 5), (widgets["trackerFFG"], 'left', 300)])

	cmds.showWindow(widgets["win"])
	cmds.window(widgets["win"], e=True, w=400, h=110)

def resetScale(*args):
	cmds.floatFieldGrp("scalePer", e=True, v1=100)
	pass

def manualScale(*args):
	#TO-DO----------------get old scale from tracker, change it relative to manual change
	#get value from field
	scalePer = cmds.floatFieldGrp(widgets["scaleFFG"] , q=True, v1=True)
	scaleVal = scalePer/100
	#scaleShapes
	sel = cmds.ls(sl=True, type="transform")
	for obj in sel:
		#decide on object type
		objShape = cmds.listRelatives(obj, s=True)
		shapeType = cmds.objectType(objShape)

		cmds.select(cl=True)
		if shapeType == "nurbsSurface" or shapeType == "nurbsCurve":
			#get the components
			cvs = cmds.select((obj + ".cv[*]"))
			cmds.scale(scaleVal, scaleVal, scaleVal)
		elif shapeType == "mesh":
			#get the components
			cvs = cmds.select((obj + ".vtx[*]"))
			cmds.scale(scaleVal, scaleVal, scaleVal)
		else:
			cmds.warning("%s isn't a nurbs or poly object, so it was skipped")

	#clear and reselect all
	cmds.select(cl=True)
	cmds.select(sel)

	pass

def shapeScaleExecute(*args):
	"""takes the components of the selected obj and scales them according the slider"""
#TO-DO---------------- get old scale from tracker, change it relative to slider
#TO-DO----------------slider should change the scale FFG to the value, THEN when you do it again, it reflects only the last change
	oldScale = cmds.floatFieldGrp(widgets["scaleFFG"], q=True, v1=True)

	#get the selected obj
	sel = cmds.ls(sl=True, type="transform")

	#get the value from the slider
	scaleVal = cmds.floatSliderGrp(widgets["slider"] , q=True, v=True)

	for obj in sel:
		#decide on object type
		objShape = cmds.listRelatives(obj, s=True)
		shapeType = cmds.objectType(objShape)

		cmds.select(cl=True)
		if shapeType == "nurbsSurface" or shapeType == "nurbsCurve":
			#get the components
			cvs = cmds.select((obj + ".cv[*]"))
			cmds.scale(scaleVal, scaleVal, scaleVal)
			#fix scale adjuster
			newScale = oldScale * scaleVal
			cmds.floatFieldGrp(widgets["scaleFFG"], e=True, v1=newScale)
		elif shapeType == "mesh":
			#get the components
			cvs = cmds.select((obj + ".vtx[*]"))
			cmds.scale(scaleVal, scaleVal, scaleVal)
			#fix scale adjuster
			newScale = oldScale * scaleVal
			cmds.floatFieldGrp(widgets["scaleFFG"], e=True, v1=newScale)
		else:
			cmds.warning("%s isn't a nurbs or poly object, so it was skipped")

	#reset slider to 1, so we don't stack scalings
	cmds.floatSliderGrp(widgets["slider"], e=True, v=1)

	#clear and reselect all
	cmds.select(cl=True)
	cmds.select(sel)

def shapeScale():
	shapeScaleUI()

