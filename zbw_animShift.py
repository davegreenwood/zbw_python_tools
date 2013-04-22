########################
#file: zbw_animShift.py
#author: zeth willie
#contact: zeth@catbuks.com, www.williework.blogspot.com
#date modified: 4/07/13
#
#notes:
########################

# select an object and capture it's initial values, these will be shown in a column (t, r, s). Then move that object around and capture the new values (these are in a second adjacent column). This will fill in an offset column. Then there's a button that will offset the curves for each attr, EXCEPT at that frame if there's a key there. You can then select another object and apply that same transformation. . . You can have option to enable the "offset" column and manually enter the offset values.

#TO-DO----------------add in time options (range, slider, all)
#TO-DO----------------make whole thing a class so I can pass info down about whether there was a key or not, etc.
#TO-DO----------------make whole thing w/ frame layout? At least make it narrower by 50 px

import maya.cmds as cmds

widgets = {}

def shiftUI(*args):
	"""ui for the module"""

	if cmds.window("shiftWin", exists=True):
		cmds.deleteUI("shiftWin")

	widgets["win"] = cmds.window("shiftWin", t="zbw_animShift", w=450, h=500)
	widgets["mainCLO"] = cmds.columnLayout()

	widgets["getBaseBut"]  = cmds.button(l="Set Base Object and Frame To Drive Shift", w=450, h=40, bgc=(.6,.8,.6), c=getBase)
	widgets["baseTFG"] = cmds.textFieldGrp(l="Base Object", cal=((1,"left"), (2,"left")), cw=((1, 100),(2,300)), ed=False)
	widgets["baseFrameFFG"] = cmds.floatFieldGrp(l="Base Frame", cal = ((1, "left"), (2,"left")), cw=((1,100), (2,50)), pre=2, en=False)
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

	widgets["origTxFFG"] = cmds.floatFieldGrp(l="tx", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modTxFFG"] = cmds.floatFieldGrp(l="tx", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["difTxFFG"] = cmds.floatFieldGrp(l="tx", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

	widgets["origTyFFG"] = cmds.floatFieldGrp(l="ty", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modTyFFG"] = cmds.floatFieldGrp(l="ty", pre=5, cal=([1,"left"], [2, "left"]),  en=False,cw=([1, 30], [2,75]))
	widgets["difTyFFG"] = cmds.floatFieldGrp(l="ty", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

	widgets["origTzFFG"] = cmds.floatFieldGrp(l="tz", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modTzFFG"] = cmds.floatFieldGrp(l="tz", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["difTzFFG"] = cmds.floatFieldGrp(l="tz", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)

	widgets["origRxFFG"] = cmds.floatFieldGrp(l="rx", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modRxFFG"] = cmds.floatFieldGrp(l="rx", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["difRxFFG"] = cmds.floatFieldGrp(l="rx", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

	widgets["origRyFFG"] = cmds.floatFieldGrp(l="ry", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modRyFFG"] = cmds.floatFieldGrp(l="ry", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["difRyFFG"] = cmds.floatFieldGrp(l="ry", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

	widgets["origRzFFG"] = cmds.floatFieldGrp(l="rz", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modRzFFG"] = cmds.floatFieldGrp(l="rz", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["difRzFFG"] = cmds.floatFieldGrp(l="rz", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)

	widgets["origSxFFG"] = cmds.floatFieldGrp(l="sx", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modSxFFG"] = cmds.floatFieldGrp(l="sx", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["difSxFFG"] = cmds.floatFieldGrp(l="sx", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

	widgets["origSyFFG"] = cmds.floatFieldGrp(l="sy", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modSyFFG"] = cmds.floatFieldGrp(l="sy", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["difSyFFG"] = cmds.floatFieldGrp(l="sy", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

	widgets["origSzFFG"] = cmds.floatFieldGrp(l="sz", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
	widgets["modSzFFG"] = cmds.floatFieldGrp(l="sz", pre=5, cal=([1,"left"], [2, "left"]), en=False,cw=([1, 30], [2,75]))
	widgets["difSzFFG"] = cmds.floatFieldGrp(l="sz", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)
	cmds.separator(style="single", h=5)

	cmds.setParent(widgets["mainCLO"])
#TO-DO----------------	#checkbox to unlock (or enable) th second and third (difference) column?

	#button to capture and calculate changes to the anim curves
	widgets["captureBut"] = cmds.button(l="Calculate and Capture Changed Values", w=450, h=40, bgc=(.8,.6,.6), c=captureChanges)
	cmds.separator(style="single", h=10)
#TO-DO----------------	#button to clear the base object (and the values)

#TO-DO----------------	#button to move the selected objects curves to the offset values
	widgets["baseMoveBut"] = cmds.button(l="Change the Anim Curves for Selected Objects!", w=450, h=40, bgc=(.6,.6,.8), c= shiftAnim)
#TO-DO----------------check and see if there is a keyframe at the current time in the orig animation
#TO-DO----------------if NOT then checkbox to see if we should keep that key (only happens on base OBJ)

#TO-DO----------------button to change OTHER objects (don't have to worry about undoing keyframes)


	cmds.showWindow(widgets["win"])
	cmds.window(widgets["win"], e=True, w=450, h=500)


#####functions
def getBase(*args):
	#TO-DO----------------here check if the indiv channels have a key on them, store this info in checkbox?
	sel = cmds.ls(sl=True, type="transform", l=True)

	if len(sel)>1:
		cmds.warning("You've selected more than one object. Only one object can be the base of the animation shift")
	else:
		obj = sel[0]
		#put sel in the base obj tfg and get the frame
		cmds.textFieldGrp(widgets["baseTFG"], e=True, tx=obj)
		frame = cmds.currentTime(q=True)
		cmds.floatFieldGrp(widgets["baseFrameFFG"], e=True, v1=frame)

		btx = cmds.getAttr("%s.tx"%obj)
		bty = cmds.getAttr("%s.ty"%obj)
		btz = cmds.getAttr("%s.tz"%obj)

		brx = cmds.getAttr("%s.rx"%obj)
		bry = cmds.getAttr("%s.ry"%obj)
		brz = cmds.getAttr("%s.rz"%obj)

		bsx = cmds.getAttr("%s.sx"%obj)
		bsy = cmds.getAttr("%s.sy"%obj)
		bsz = cmds.getAttr("%s.sz"%obj)

		cmds.floatFieldGrp(widgets["origTxFFG"], e=True, v1=btx)
		cmds.floatFieldGrp(widgets["origTyFFG"], e=True, v1=bty)
		cmds.floatFieldGrp(widgets["origTzFFG"], e=True, v1=btz)

		cmds.floatFieldGrp(widgets["origRxFFG"], e=True, v1=brx)
		cmds.floatFieldGrp(widgets["origRyFFG"], e=True, v1=bry)
		cmds.floatFieldGrp(widgets["origRzFFG"], e=True, v1=brz)

		cmds.floatFieldGrp(widgets["origSxFFG"], e=True, v1=bsx)
		cmds.floatFieldGrp(widgets["origSyFFG"], e=True, v1=bsy)
		cmds.floatFieldGrp(widgets["origSzFFG"], e=True, v1=bsz)

def captureChanges(*args):
		obj = cmds.textFieldGrp(widgets["baseTFG"], q=True, tx=True)
		frame = cmds.floatFieldGrp(widgets["baseFrameFFG"], q=True, v1=True)
		cmds.currentTime(frame, edit=True)

		#poplulate the second column with the new values from the base object
		mtx = cmds.getAttr("%s.tx"%obj)
		mty = cmds.getAttr("%s.ty"%obj)
		mtz = cmds.getAttr("%s.tz"%obj)

		mrx = cmds.getAttr("%s.rx"%obj)
		mry = cmds.getAttr("%s.ry"%obj)
		mrz = cmds.getAttr("%s.rz"%obj)

		msx = cmds.getAttr("%s.sx"%obj)
		msy = cmds.getAttr("%s.sy"%obj)
		msz = cmds.getAttr("%s.sz"%obj)

		cmds.floatFieldGrp(widgets["modTxFFG"], e=True, v1=mtx)
		cmds.floatFieldGrp(widgets["modTyFFG"], e=True, v1=mty)
		cmds.floatFieldGrp(widgets["modTzFFG"], e=True, v1=mtz)

		cmds.floatFieldGrp(widgets["modRxFFG"], e=True, v1=mrx)
		cmds.floatFieldGrp(widgets["modRyFFG"], e=True, v1=mry)
		cmds.floatFieldGrp(widgets["modRzFFG"], e=True, v1=mrz)

		cmds.floatFieldGrp(widgets["modSxFFG"], e=True, v1=msx)
		cmds.floatFieldGrp(widgets["modSyFFG"], e=True, v1=msy)
		cmds.floatFieldGrp(widgets["modSzFFG"], e=True, v1=msz)

		#get orig values
		otx = cmds.floatFieldGrp(widgets["origTxFFG"], q=True, v1=True)
		oty = cmds.floatFieldGrp(widgets["origTyFFG"], q=True, v1=True)
		otz = cmds.floatFieldGrp(widgets["origTzFFG"], q=True, v1=True)

		orx = cmds.floatFieldGrp(widgets["origRxFFG"], q=True, v1=True)
		ory = cmds.floatFieldGrp(widgets["origRyFFG"], q=True, v1=True)
		orz = cmds.floatFieldGrp(widgets["origRzFFG"], q=True, v1=True)

		osx = cmds.floatFieldGrp(widgets["origSxFFG"], q=True, v1=True)
		osy = cmds.floatFieldGrp(widgets["origSyFFG"], q=True, v1=True)
		osz = cmds.floatFieldGrp(widgets["origSzFFG"], q=True, v1=True)

		#now subtract them and put the value in the diff column
		dtx = mtx - otx
		dty = mty - oty
		dtz = mtz - otz

		drx = mrx - orx
		dry = mry - ory
		drz = mrz - orz

		dsx = msx - osx
		dsy = msy - osy
		dsz = msz - osz

		cmds.floatFieldGrp(widgets["difTxFFG"], e=True, v1=dtx)
		cmds.floatFieldGrp(widgets["difTyFFG"], e=True, v1=dty)
		cmds.floatFieldGrp(widgets["difTzFFG"], e=True, v1=dtz)

		cmds.floatFieldGrp(widgets["difRxFFG"], e=True, v1=drx)
		cmds.floatFieldGrp(widgets["difRyFFG"], e=True, v1=dry)
		cmds.floatFieldGrp(widgets["difRzFFG"], e=True, v1=drz)

		cmds.floatFieldGrp(widgets["difSxFFG"], e=True, v1=dsx)
		cmds.floatFieldGrp(widgets["difSyFFG"], e=True, v1=dsy)
		cmds.floatFieldGrp(widgets["difSzFFG"], e=True, v1=dsz)


def shiftAnim(*args):
	#TO-DO----------------if obj is base then check about that key on the base frame
	#get vals of changes for each
	dtx = cmds.floatFieldGrp(widgets["difTxFFG"], q=True, v1=True)
	dty = cmds.floatFieldGrp(widgets["difTyFFG"], q=True, v1=True)
	dtz = cmds.floatFieldGrp(widgets["difTzFFG"], q=True, v1=True)

	drx = cmds.floatFieldGrp(widgets["difRxFFG"], q=True, v1=True)
	dry = cmds.floatFieldGrp(widgets["difRyFFG"], q=True, v1=True)
	drz = cmds.floatFieldGrp(widgets["difRzFFG"], q=True, v1=True)

	dsx = cmds.floatFieldGrp(widgets["difSxFFG"], q=True, v1=True)
	dsy = cmds.floatFieldGrp(widgets["difSyFFG"], q=True, v1=True)
	dsz = cmds.floatFieldGrp(widgets["difSzFFG"], q=True, v1=True)

	sel = cmds.ls(sl=True, type="transform", l=True)

	for obj in sel:
		cmds.keyframe(sel, at=("tx"), r=True, vc=dtx)
		cmds.keyframe(sel, at=("ty"), r=True, vc=dty)
		cmds.keyframe(sel, at=("tz"), r=True, vc=dtz)

		cmds.keyframe(sel, at=("rx"), r=True, vc=drx)
		cmds.keyframe(sel, at=("ry"), r=True, vc=dry)
		cmds.keyframe(sel, at=("rz"), r=True, vc=drz)

		cmds.keyframe(sel, at=("sx"), r=True, vc=dsx)
		cmds.keyframe(sel, at=("sy"), r=True, vc=dsy)
		cmds.keyframe(sel, at=("sz"), r=True, vc=dsz)
#BELOW IS ONLY IF obj is base obj
#TO-DO----------------if the anim curve HAD a key at the base frame, offset it back by the neg value of the delta
#TO-DO----------------if NOT then delete the key here

def clearBase(*args):
	pass

def enableDiff(*args):
	pass


def animShift(*args):
	shiftUI()