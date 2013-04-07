########################
#file: zbw_appendPath.py
#author: zeth willie
#contact: zeth@catbuks.com, www.williework.blogspot.com
#date modified: 01/15/13
#
#notes: put this in your scripts folder. use "import zbw_appendPath", then "zbw_appendPath.appendPath()"
########################


#TO-DO----------------add option in second tab to move path up or down the stack, maybe also move to top (pop out of list?)

import sys, os
import maya.cmds as cmds
from functools import partial

widgets = {}

def appendUI():
	#create window with 3 text fields, buttons call up proc to add path
	if cmds.window("appendPath", exists=True):
		cmds.deleteUI("appendPath")

	widgets["win"] = cmds.window("appendPath", t="zbw_appendPath", w=500, h=170)

	#create some menus for saving and loading
	cmds.setParent(widgets["win"])
	widgets["menu"] = cmds.menuBarLayout()
	widgets["menuFile"] = cmds.menu(label="file")
	cmds.menuItem(l='Clear Values', c=clearValues)
	cmds.menuItem(l="Save Add Paths", c=saveValues)
	cmds.menuItem(l="Load Add Paths", c=loadValues)

	widgets["tabLO"] = cmds.tabLayout(h=170)
	widgets["columnLO"] = cmds.columnLayout("Add Paths", w=500, h=170)
	widgets["path1"] = cmds.textFieldButtonGrp(l="path1", cal=[(1, "left"), (2,"left"),(3,"left")], cw3=(40, 410, 50), bl="<<<", bc=partial(addToField, 1))
	widgets["path2"] = cmds.textFieldButtonGrp(l="path2", cal=[(1, "left"), (2,"left"),(3,"left")], cw3=(40, 410, 50), bl="<<<", bc=partial(addToField, 2))
	widgets["path3"] = cmds.textFieldButtonGrp(l="path3", cal=[(1, "left"), (2,"left"),(3,"left")], cw3=(40, 410, 50), bl="<<<", bc=partial(addToField, 3))
	cmds.separator(h=10, st="single")
	widgets["AddBut"] = cmds.button(l="Add paths to sys.path", w=500, h=40, bgc=(.6, .5, .5), c=append)
	#back to window
	cmds.setParent(widgets["tabLO"])
	widgets["columnLO2"] = cmds.columnLayout("View Paths", w=500, h=100)
	widgets["listTSL"] = cmds.textScrollList(w=500, h=100, fn="smallPlainLabelFont", append=["click button below", "to refresh this list!"], dcc=printMe)
	refresh()
	widgets["columnLO3"] = cmds.columnLayout(w=500, h=50)
	widgets["refreshBut"] = cmds.button(l="Refresh Paths", w=500, h=40, bgc=(.5, .5, .6), c=refresh)

	#load (and check) previous saves


	cmds.showWindow(widgets["win"])
	cmds.window(widgets["win"], e=True, w=500, h=170)

def addToField(num, *args):
	#set the field to add to
	textField  = widgets["path%s"%num]

	#call up browser to look for paths
	path = cmds.fileDialog2(fm=3)[0]

	#add text
	if path:
		cmds.textFieldButtonGrp(textField, e=True, tx=path)


def printMe():
	#get text at selected index
	sel = cmds.textScrollList(widgets["listTSL"], q=True, si=True)

	#print that text to script editor
	print sel[0]

def append(*args):
	paths = []

	#get paths
	path1 = cmds.textFieldButtonGrp(widgets["path1"], q=True, tx=True)
	path2 = cmds.textFieldButtonGrp(widgets["path2"], q=True, tx=True)
	path3 = cmds.textFieldButtonGrp(widgets["path3"], q=True, tx=True)
	paths.append(path1)
	paths.append(path2)
	paths.append(path3)

	#append path with text from fields
	check = 0
	for path in paths:
		if path:
			if os.path.isdir(path):
				sys.path.append(path)
				check += 1
			else:
				cmds.warning("%s is not an existing path and wasn't added to sys.path"%path)
	if check > 0:
		cmds.warning("Added paths! Check the 'View Paths' tab to see them")

	#delete the text
	cmds.textFieldButtonGrp(widgets["path1"], e=True, tx="")
	cmds.textFieldButtonGrp(widgets["path2"], e=True, tx="")
	cmds.textFieldButtonGrp(widgets["path3"], e=True, tx="")

	#refresh the path list on second tab
	refresh()

def refresh(*args):
	#delete anything in the list
	cmds.textScrollList(widgets["listTSL"], edit=True, ra=True)

	#get the sys.path
	pathList = sys.path

	#add each element to list
	for path in pathList:
		cmds.textScrollList(widgets["listTSL"], edit=True, append=[path])

def clearValues(*args):
	cmds.textFieldButtonGrp(widgets["path1"], e=True, tx="")
	cmds.textFieldButtonGrp(widgets["path2"], e=True, tx="")
	cmds.textFieldButtonGrp(widgets["path3"], e=True, tx="")

def loadValues(*args):
	#check if file exists
	try:
		userDir = cmds.internalVar(upd=True) + "zbw_appendPathSave.txt"
		file = open(userDir, "r")
		paths = []
		#read values from file to list
		for line in file:
			paths.append(line.rstrip("\n"))
		file.close()

		#replace tfbg's with those values
		cmds.textFieldButtonGrp(widgets["path1"], e=True, tx=paths[0])
		cmds.textFieldButtonGrp(widgets["path2"], e=True, tx=paths[1])
		cmds.textFieldButtonGrp(widgets["path3"], e=True, tx=paths[2])
	except IOError:
		cmds.warning("You don't seem to have a 'zbw_appendPathSave.txt' file saved in your user prefs dir")

def saveValues(*args):
	path1 = cmds.textFieldButtonGrp(widgets["path1"], q=True, tx=True) + "\n"
	path2 = cmds.textFieldButtonGrp(widgets["path2"], q=True, tx=True) + "\n"
	path3 = cmds.textFieldButtonGrp(widgets["path3"], q=True, tx=True) + "\n"

	#write to file
	userDir = cmds.internalVar(upd=True) + "zbw_appendPathSave.txt"
	file = open(userDir, "w")

	file.write(path1)
	file.write(path2)
	file.write(path3)

	file.close()

def appendPath(*args):
	appendUI()