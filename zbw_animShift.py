########################
#file: zbw_animShift.py
#author: zeth willie
#contact: zeth@catbuks.com, www.williework.blogspot.com
#date modified: 4/07/13
#
#notes: 
########################

# select an object and capture it's initial values, these will be shown in a column (t, r, s). Then move that object around and capture the new values (these are in a second adjacent column). This will fill in an offset column. Then there's a button that will offset the curves for each attr, EXCEPT at that frame if there's a key there. You can then select another object and apply that same transformation. . . You can have option to enable the "offset" column and manually enter the offset values. 

import maya.cmds as cmds

widgets = {}

def shiftUI(*args):
	"""ui for the module"""

	if cmds.window("shiftWin", exists=True):
		cmds.deleteUI("shiftWin")

	widgets["win"] = cmds.window("shiftWin", t="zbw_animShift", w=450, h=400)
	widgets["mainCLO"] = cmds.columnLayout()

	widgets["getBaseBut"]  = cmds.button(l="Get Base Object To Drive Shift", w=450, h=40, bgc=(.6,.8,.6), c=getBase)
	widgets["baseTFG"] = cmds.textFieldGrp(l="Base Object", cal=((1,"left"), (2,"left")), cw=((1, 100),(2,300)))
#TO-DO----------------add frame counter to know what frame you grabbed the values from (and to go back there to calc the differences.). Maybe button to take you back there
	cmds.separator(h=10)

	widgets["valueRCL"] = cmds.rowColumnLayout(nc=3, cw=([1,150],[2,150],[3,150])) #or do formLayout with 3 columns
	#create the columns for the three different fields we'll need (left=orig, mid=changed, right=diff)
	cmds.text("Orig Values")
	cmds.text("Modified Values")
	cmds.text("Difference Value")
	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)

	widgets["origTxFFG"] = cmds.floatFieldGrp(l="tx", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modTxFFG"] = cmds.floatFieldGrp(l="tx", cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))
	widgets["difTxFFG"] = cmds.floatFieldGrp(l="tx", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))

	widgets["origTyFFG"] = cmds.floatFieldGrp(l="ty", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modTyFFG"] = cmds.floatFieldGrp(l="ty", cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))
	widgets["difTyFFG"] = cmds.floatFieldGrp(l="ty", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))

	widgets["origTzFFG"] = cmds.floatFieldGrp(l="tz", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modTzFFG"] = cmds.floatFieldGrp(l="tz", cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))
	widgets["difTzFFG"] = cmds.floatFieldGrp(l="tz", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))

	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)

	widgets["origRxFFG"] = cmds.floatFieldGrp(l="rx", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modRxFFG"] = cmds.floatFieldGrp(l="rx", cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))
	widgets["difRxFFG"] = cmds.floatFieldGrp(l="rx", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))

	widgets["origRyFFG"] = cmds.floatFieldGrp(l="ry", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modRyFFG"] = cmds.floatFieldGrp(l="ry", cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))
	widgets["difRyFFG"] = cmds.floatFieldGrp(l="ry", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))

	widgets["origRzFFG"] = cmds.floatFieldGrp(l="rz", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modRzFFG"] = cmds.floatFieldGrp(l="rz", cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))
	widgets["difRzFFG"] = cmds.floatFieldGrp(l="rz", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))

	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)

	widgets["origSxFFG"] = cmds.floatFieldGrp(l="sx", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modSxFFG"] = cmds.floatFieldGrp(l="sx", cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))
	widgets["difSxFFG"] = cmds.floatFieldGrp(l="sx", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))

	widgets["origSyFFG"] = cmds.floatFieldGrp(l="sy", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modSyFFG"] = cmds.floatFieldGrp(l="sy", cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))
	widgets["difSyFFG"] = cmds.floatFieldGrp(l="sy", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))

	widgets["origSzFFG"] = cmds.floatFieldGrp(l="sz", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modSzFFG"] = cmds.floatFieldGrp(l="sz", cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))
	widgets["difSzFFG"] = cmds.floatFieldGrp(l="sz", cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))

	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)

	#checkbox to unlock (or enable) th second and third (difference) column
	
	#create two buttons for the function (first will capture the values at the current time(and the name of the base object), second will add the new changed values to the second column and calc the difference in the third)

	#textfield that holds the name of the base object (should be un-enabled)

	#button to clear the base object (and the values)

	#button to move the selected objects curves to the offset values



	cmds.showWindow(widgets["win"])
	cmds.window(widgets["win"], e=True, w=450, h=400)


#####functions
def getBase(*args):
	pass
#get the selected and populate the first columns with the transforms (save name of object)
def lockChanges(*args):
	pass
#get the new moved positions and populate the second list with transforms and then calculate the third list with differences

def shiftAnim(*args):
	pass
#grab the anim curves for the selected objects and move them relative to the diff column, for the saved name set the values at that location in the new location for all (will this obviate the need for excluding this from the curve move? set key there?  test against no auto-keyframe)

def clearBase(*args):
	pass

def enableDiff(*args):
	pass


def animShift(*args):
	shiftUI()