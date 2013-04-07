# select an object and capture it's initial values, these will be shown in a column (t, r, s). Then move that object around and capture the new values (these are in a second adjacent column). This will fill in an offset column. Then there's a button that will offset the curves for each attr, EXCEPT at that frame if there's a key there. You can then select another object and apply that same transformation. . . You can have option to enable the "offset" column and manually enter the offset values. 

import maya.cmds as cmds

widgets = {}

def shiftUI(*args):
	"""ui for the module"""

	if cmds.window("shiftWin", exists=True):
		cmds.deleteUI("shiftWin")

	widgets["win"] = cmds.window("shiftWin", w=400, h=400)
	widgets["mainCLO"] = cmds.columnLayout()

	widgets["mainFLO"] = cmds.formLayout() #or do rowColumnLayout with 3 columns
	#create the columns for the three different fields we'll need (left=orig, mid=changed, right=diff)

	#checkbox to unlock (or enable) the third (difference) column

	#create two buttons for the function (first will capture the values at the current time(and the name of the base object), second will add the new changed values to the second column and calc the difference in the third)

	#textfield that holds the name of the base object (should be un-enabled)

	#button to clear the base object (and the values)

	#button to move the selected objects curves to the offset values



	cmds.showWindow(widgets["win"])
	cmds.window(widgets["win"], e=True, w=400, h=400)


#####functions
def getBase(*args):
	pass
#get the selected and populate the first columns with the transforms (save name of object)
def lockChanges(*args):
	pass
#get the new moved positions and populate the second list with transforms and then calculate the third list with differences

def shiftAnim(*args):
	pass
#grab the anim curves for the selected objects and move them relative to the diff column, for the saved name set the keyframe at that location in the new location for all? 

def clearBase(*args):
	pass

def enableDiff(*args):
	pass


def animShift(*args):
	shiftUI()