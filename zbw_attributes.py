########################
#file: zbw_attributes.py
#author: zeth willie
#contact: zeth@catbuks.com, www.williework.blogspot.com
#date modified: 1/26/13
#
#notes: some basic stuff for everyday rigging, etc
########################

import maya.cmds as cmds
from functools import partial
import maya.mel as mel

#TO-DO----------------add "breakConnections"? disconnect and if they're anim curves delete them.

widgets = {}
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

def attrUI(*args):
	if cmds.window("attrWin", exists=True):
		cmds.deleteUI("attrWin")

	widgets["win"] = cmds.window("attrWin", t="zbw_attributes", h=370, w=250, s=True)
	widgets["tabLO"] = cmds.tabLayout()
	widgets["channelColLO"] = cmds.columnLayout("Object/Attr Controls", w=250, bgc=(.8,.8,.8))

	widgets["lockFrLO"] = cmds.frameLayout(l="Lock/Hide", cll=True, w=250, bgc=(.7,.6,.6))
	widgets["lockColLO"] = cmds.columnLayout(bgc=(.8,.8,.8))
	#lock and hide controls
	widgets["channelCBG"] = cmds.checkBoxGrp(w=250, cw4=(60,60,60,60), ncb=4, l1="Trans", l2="Rot", l3="Scale", l4="Vis", va4=(0,0,1,1))
	widgets["lockRBG"] = cmds.radioButtonGrp(nrb=2, l1="Unlock", l2="Lock", sl=2)
	widgets["hideRBG"] = cmds.radioButtonGrp(nrb=2, l1="Show", l2="Hide", sl=2)
	widgets["channelsBut"] = cmds.button(l="Lock/Hide Channels", w=150, h=30, bgc=(.5,.5,.5), rs=True, c=channelLockHide)
	cmds.separator(h=5, st="none")

	cmds.setParent(widgets["channelColLO"])
	widgets["colorFrLO"] = cmds.frameLayout(l="Object Color", cll=True, w=250, bgc=(.7,.6,.6))
	widgets["colorRCLO"] = cmds.rowColumnLayout(nr=4, bgc=(.8,.8,.8))
	#color controls (red, green, blue, yellow, other)
	cmds.canvas(w=50, h=20, rgb=(1,0,0), pc=partial(changeColor, colors["red"]))
	cmds.canvas(w=50, h=20, rgb=(.5,.1,.1), pc=partial(changeColor, colors["darkRed"]))
	cmds.canvas(w=50, h=20, rgb=(.659,.275,.449), pc=partial(changeColor, colors["lightRed"]))
	cmds.canvas(w=50, h=20, rgb=(1,.8,.965), pc=partial(changeColor, colors["pink"]))

	cmds.canvas(w=50, h=20, rgb=(0,1,0), pc=partial(changeColor, colors["green"]))
	cmds.canvas(w=50, h=20, rgb=(0,.35,0), pc=partial(changeColor, colors["darkGreen"]))
	cmds.canvas(w=50, h=20, rgb=(0,.55,.335), pc=partial(changeColor, colors["medGreen"]))
	cmds.canvas(w=50, h=20, rgb=(.35,.635,.15), pc=partial(changeColor, colors["yellowGreen"]))

	cmds.canvas(w=50, h=20, rgb=(0,0,1), pc=partial(changeColor, colors["blue"]))
	cmds.canvas(w=50, h=20, rgb=(0,0,.35), pc=partial(changeColor, colors["darkBlue"]))
	cmds.canvas(w=50, h=20, rgb=(0,.2,.6), pc=partial(changeColor, colors["medBlue"]))
	cmds.canvas(w=50, h=20, rgb=(.65,.8,1), pc=partial(changeColor, colors["lightBlue"]))

	cmds.canvas(w=50, h=20, rgb=(1,1,0), pc=partial(changeColor, colors["yellow"]))
	cmds.canvas(w=50, h=20, rgb=(.225,.1,0), pc=partial(changeColor, colors["darkBrown"]))
	cmds.canvas(w=50, h=20, rgb=(.5,.275,0), pc=partial(changeColor, colors["brown"]))
	cmds.canvas(w=50, h=20, rgb=(.922,.707,.526), pc=partial(changeColor, colors["darkYellow"]))

	cmds.canvas(w=50, h=20, rgb=(.33,0,.33), pc=partial(changeColor, colors["purple"]))
	cmds.canvas(w=50, h=20, rgb=(.2,0,.25), pc=partial(changeColor, colors["darkPurple"]))
	cmds.canvas(w=50, h=20, rgb=(.0,0,.0), pc=partial(changeColor, colors["black"]))
	cmds.canvas(w=50, h=20, rgb=(1,1,1), pc=partial(changeColor, colors["white"]))

#TO-DO----------------figure out breaking connections(to delete or not?), call add attr win
	# cmds.setParent(widgets["channelColLO"])
	# widgets["channelFrLO"] = cmds.frameLayout(l="Channels", cll=True, w=250, bgc=(1,1,1))
	# widgets["channelRCLO"] = cmds.columnLayout(bgc=(.8,.8,.8))
	# widgets["breakAllBut"] = cmds.button(l="Break All Connections", w=150, h=30, bgc=(.5,.5,.5))
	# widgets["breakSelBut"] = cmds.button(l="Break Selected Connections", w=150, h=30, bgc=(.5,.5,.5))
	# cmds.separator(h=10, st="none")
	# widgets["addAttBut"] = cmds.button(l="Show 'Add Attribute' win", w=150, h=30, bgc=(.5,.5,.5))

	cmds.setParent(widgets["tabLO"])
	widgets["connectColLO"] = cmds.columnLayout("Connections", w=250, bgc=(.8,.8,.8))
	widgets["connectFrame"] = cmds.frameLayout(l="Make General Connections", cll=True, bgc=(.6,.8,.6))
	widgets["connectionColLO"] = cmds.columnLayout(bgc=(.8,.8,.8))

	#connection stuff
	cmds.text("Select a source object and a channel:")
	widgets["connector"] = cmds.textFieldButtonGrp(l="Connector", w=250, bl="<<<", cal=[(1,"left"),(2,"left"),(3,"left")], cw3=[60,140,30], bc=partial(getChannel, "connector"))
	cmds.separator(h=5,st="none")
	cmds.text("Select a target object and channel:")
	widgets["connectee"] = cmds.textFieldButtonGrp(l="Connectee", w=250, bl="<<<", cal=[(1,"left"),(2,"left"),(3,"left")], cw3=[60,140,30], bc=partial(getChannel, "connectee"))
	cmds.separator(h=10,st="none")
	widgets["connectBut"] = cmds.button(l="Connect Two Channels", w=240, h=30, bgc=(.5,.5,.5), c=connectChannels)
	cmds.separator(h=5,st="none")

	cmds.setParent(widgets["connectColLO"])
	widgets["shapeFrame"] = cmds.frameLayout(l="Connect to Shape Visibility", cll=True, bgc=(.6,.8,.6))
	widgets["shapeColLO"] = cmds.columnLayout(bgc=(.8,.8,.8))

	widgets["toShapeVis"] = cmds.textFieldButtonGrp(l="Vis Driver", w=250, bl="<<<", cal=[(1,"left"),(2,"left"),(3,"left")], cw3=[60,140,30], bc=partial(getChannel, "toShapeVis"))
	cmds.separator(h=5,st="none")
	cmds.text("Now select the objs to drive:")
	widgets["shapeBut"] = cmds.button(l="Connect to Shapes' vis", w=240, h=30, bgc=(.5,.5,.5), c=connectShapeVis)
	cmds.separator(h=5,st="none")

	cmds.setParent(widgets["connectColLO"])
	widgets["inoutFrame"] = cmds.frameLayout(l="Select Connections (and print)", cll=True, bgc=(.6,.8,.6))
	widgets["inOutColLO"] = cmds.columnLayout(bgc=(.8,.8,.8))

	widgets["conversionCB"] = cmds.checkBox(l="Skip 'conversion' nodes?", v=1)
	cmds.text("Select an attribute in the channel box:")
	widgets["getInputBut"] = cmds.button(l="Select inConnection object", w=240, h=30, bgc=(.5,.5,.5), c=getInput)
	widgets["getOutputBut"] = cmds.button(l="Select outConnection objects", w=240, h=30, bgc=(.5,.5,.5), c=getOutput)

	#show window
	cmds.showWindow(widgets["win"])
	cmds.window(widgets["win"], e=True, w=250, h=370)

def channelLockHide(*args):
	sel = cmds.ls(sl=True, type="transform")
	if sel:
		channels = []
		t = cmds.checkBoxGrp(widgets["channelCBG"], q=True, v1=True)
		r = cmds.checkBoxGrp(widgets["channelCBG"], q=True, v2=True)
		s = cmds.checkBoxGrp(widgets["channelCBG"], q=True, v3=True)
		v = cmds.checkBoxGrp(widgets["channelCBG"], q=True, v4=True)
		lock = cmds.radioButtonGrp(widgets["lockRBG"], q=True, sl=True)
		key = cmds.radioButtonGrp(widgets["hideRBG"], q=True, sl=True)
		if lock == 1:
			lock = 0
		elif lock == 2:
			lock = 1
		if key == 1:
			key = 1
		elif key == 2:
			key = 0

		trans = [".tx", ".ty", ".tz"]
		rot = [".rx", ".ry", ".rz"]
		scale = [".sx", ".sy", ".sz"]
		vis = [".v"]

		if t:
			channels.extend(trans)
		if r:
			channels.extend(rot)
		if s:
			channels.extend(scale)
		if v:
			channels.extend(vis)

		for obj in sel:
			for channel in channels:
				cmds.setAttr((obj+channel), l=lock)
				cmds.setAttr((obj+channel), k=key)

def changeColor(color, *args):
	sel = cmds.ls(sl=True, type="transform")
	if sel:
		for obj in sel:
			shapes = cmds.listRelatives(obj, s=True)
			for shape in shapes:
				cmds.setAttr("%s.overrideEnabled"%shape, 1)
				cmds.setAttr("%s.overrideColor"%shape, color)

def breakConnections(*args):
	#disconnectAttr
	pass

def getChannel(tfbg, *args):
	obj = ""
	channel = ""

	cBox = mel.eval('$temp=$gChannelBoxName')
	sel = cmds.ls(sl=True, l=True)

	if sel:
		if not len(sel)==1:
			cmds.warning("You have to select ONE node!")
		else:
			obj = sel[0]
	else:
		cmds.warning("You have to select ONE node!")

	if sel:
		channels = cmds.channelBox(cBox, q=True, sma=True, ssa=True, sha=True, soa=True)

		if channels:
			if not len(channels) == 1:
				cmds.warning("You have to select ONE channel!")
			else:
				channel = channels[0]
		else:
			cmds.warning("You have to select ONE channel!")

	if obj and channel:
		full = "%s.%s"%(obj, channel)
		cmds.textFieldButtonGrp(widgets[tfbg], e=True, tx=full)

def connectChannels(*args):
	connector = cmds.textFieldButtonGrp(widgets["connector"], q=True, tx=True)
	connectee = cmds.textFieldButtonGrp(widgets["connectee"], q=True, tx=True)
	try:
		cmds.connectAttr(connector, connectee, f=True)
		print "Connected %s -----> %s"%(connector, connectee)
	except:
		cmds.warning("Couldn't connect those attrs. . . Sorry!")

def getInput(*args):
	obj = ""
	channel = ""
	conv = cmds.checkBox(widgets["conversionCB"], q=True, v=True)

	cBox = mel.eval('$temp=$gChannelBoxName')
	sel = cmds.ls(sl=True, l=True)

	if sel:
		if not len(sel)==1:
			cmds.warning("You have to select ONE node!")
		else:
			obj = sel[0]
	else:
		cmds.warning("You have to select ONE node!")

	if sel:
		channels = cmds.channelBox(cBox, q=True, sma=True, ssa=True, sha=True, soa=True)

		if channels:
			if not len(channels) == 1:
				cmds.warning("You have to select ONE channel!")
			else:
				channel = channels[0]
		else:
			cmds.warning("You have to select ONE channel!")

	if obj and channel:
		full = "%s.%s"%(obj, channel)
		inAttr = cmds.listConnections(full, plugs=True, scn=conv, d=False, s=True)
		if inAttr:
			for each in inAttr:
				print "%s -----> %s"%(each, full)
		else:
			cmds.warning("No input connections on this attr!")
		inNodes = cmds.listConnections(full, scn=conv, d=False, s=True)
		if inNodes:
			cmds.select(cl=True)
			for node in inNodes:
				cmds.select(node, add=True)

def getOutput(*args):
	obj = ""
	channel = ""
	conv = cmds.checkBox(widgets["conversionCB"], q=True, v=True)

	cBox = mel.eval('$temp=$gChannelBoxName')
	sel = cmds.ls(sl=True, l=True)

	if sel:
		if not len(sel)==1:
			cmds.warning("You have to select ONE node!")
		else:
			obj = sel[0]
	else:
		cmds.warning("You have to select ONE node!")

	if sel:
		channels = cmds.channelBox(cBox, q=True, sma=True, ssa=True, sha=True, soa=True)

		if channels:
			if not len(channels) == 1:
				cmds.warning("You have to select ONE channel!")
			else:
				channel = channels[0]
		else:
			cmds.warning("You have to select ONE channel!")

	if obj and channel:
		full = "%s.%s"%(obj, channel)
		outAttr = cmds.listConnections(full, plugs=True, scn=conv, d=True, s=False)
		if outAttr:
			for each in outAttr:
				print "%s ----> %s"%(full,each)
		else:
			cmds.warning("No output connections on this attr!")
		outNodes = cmds.listConnections(full, scn=conv, d=True, s=False)
		if outNodes:
			cmds.select(cl=True)
			for node in outNodes:
				cmds.select(node, add=True)

def connectShapeVis(*args):
	sel = cmds.ls(sl=True, type="transform")
	driver = cmds.textFieldButtonGrp(widgets["toShapeVis"], q=True, tx=True)

	if sel:
		if driver:
			for obj in sel:
				shapes = cmds.listRelatives(obj, s=True)
				for shape in shapes:
					try:
						cmds.connectAttr(driver, "%s.v"%shape, f=True)
						cmds.warning("Connected %s to %s"%(driver, shape))
					except:
						cmds.warning("Couldn't connect %s to %s. Sorry! Check the Script Editor."%(driver, shape))
	else:
		cmds.warning("You need to select an object to connect the shape.vis!")
def attributes(*args):
	attrUI()