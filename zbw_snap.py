########################
#file: zbw_snap.py
#Author: zeth willie
#Contact: zeth@catbuks.com, www.williework.blogspot.com
#Date Modified: 05/02/13
#To Use: type in python window  "import zbw_snap; zbw_snap.snap()"
#Notes/Descriptions: use to simply snap one object to another. Option for translate, rotate or both
########################

#TO-DO----------------make little UI
#TO-DO----------------options - snap to last or average? for multiselect

import maya.cmds as cmds

widgets = {}

def snapUI():
	if cmds.window("snapWin", exists=True):
		cmds.deleteUI("snapWin", window=True)
		cmds.windowPref("snapWin", remove=True)

	widgets["win"] = cmds.window("snapWin", t="zbw_snap", w=200, h=100)
	widgets["mainCLO"] = cmds.columnLayout(w=200, h=100)
	cmds.text("Select the target object,\nthen the object you want to snap", al="center")
	cmds.separator(h=5, style="single")
	widgets["cbg"] = cmds.checkBoxGrp(l="Options: ", ncb=2, v1=1, v2=1, l1="Translate", l2="Rotate", cal=[(1,"left"),(2,"left"), (3,"left")], cw=[(1,50),(2,75),(3,75)])
	cmds.separator(h=5, style="single")
	widgets["snapButton"] = cmds.button(l="Snap!", w=200, h=30, bgc=(.6,.8,.6), c=snapIt)

	cmds.showWindow(widgets["win"])
	cmds.window(widgets["win"], e=True, w=200, h=100)


def snapIt(*args):
	translate = cmds.checkBoxGrp(widgets["cbg"], q=True, v1=True)
	rotate = cmds.checkBoxGrp(widgets["cbg"], q=True, v2=True)

	sel = cmds.ls(sl=True)

	target = sel[0]
	object = sel[1]

#TO-DO----------------look at using something to get ws values independent of rot orders, instead of constraints
	if translate:
		pc = cmds.pointConstraint(target, object)
		cmds.delete(pc)

	if rotate:
		oc = cmds.orientConstraint(target, object)
		cmds.delete(oc)

	cmds.select(sel[1])

def snap(*args):
	snapUI()