import maya.cmds as cmds
import maya.mel as mel
#This goes (on Mac): ~/Library/Preferences/Autodesk/maya/<version>/prefs/scripts/


#on load evalDeferred() the set project script
def setProjectUI():
	if cmds.window("projectWin", exists=True):
		cmds.deleteUI("projectWin")

	win = cmds.window("projectWin", t="Set Project", w=450, h=100)
	cmds.columnLayout("CLO")
	current = getCurrent()#is this the best way to do this?
	cmds.textFieldGrp("currTFG", l="Current Project:", tx=current, ed=False, cw=[(1, 100),(2, 300), (3,50)], cal=[(1,"left"),(2,"left"),(3,"left")])
	cmds.separator(h=10, style = "single")
	cmds.textFieldButtonGrp("TFBG", l="Select Project Path: ", bl="<<<", cw=[(1, 100),(2, 300), (3,50)], cal=[(1,"left"),(2,"left"),(3,"left")], bc=getLoc )
	cmds.separator(h=10, style="single")
	cmds.rowColumnLayout(nc=2, cw=[(1,300), (2,150)])
	cmds.button("doBut", l="Change/Set Project Location!", w=300, h=30, bgc=(.6,.8,.6), c=setProject)
	cmds.button("closeBut", l="Close Window", w=150, bgc=(.8,.6,.6), c=closeWin)

	cmds.showWindow(win)
	cmds.window(win, e=True, w=450, h=100)

def setProject(*args):
	#set the project to the value in the TFBG
	path = cmds.textFieldButtonGrp("TFBG", q=True, tx=True)
	mel.eval("setProject \""+path+"\"")
	cmds.workspace(q=True, fn=True)
	#closeUI
	cmds.deleteUI("projectWin")
	cmds.warning("You've set the the current project to: %s"%path)

def getCurrent():
	#get current project
	currProj = cmds.workspace(q=True, fn=True)
	return(currProj)

def getLoc():
	#fileDialog2 to get folder
	path = cmds.fileDialog2(ds=2, fm=3)
	#put that in the text field
	cmds.textFieldButtonGrp("TFBG", e=True, tx=path[0])

def closeWin(*args):
	cmds.deleteUI("projectWin")

#create a scriptJob the looks for a new scene or open scene and runs same script
newJobNum = cmds.scriptJob(event=["NewSceneOpened", setProjectUI])
openJobNum = cmds.scriptJob(event=["SceneOpened", setProjectUI])