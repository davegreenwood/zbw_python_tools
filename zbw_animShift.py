########################
#file: zbw_animShift.py
#author: zeth willie
#contact: zeth@catbuks.com, www.williework.blogspot.com
#date modified: 4/23/13
#
#notes:
########################

#TO-DO------ ----------add in time options (range, slider, all) to UI and then to the rest of the script

import maya.cmds as cmds

class AnimShift(object):

	def __init__(self):

		self.widgets = {}
		self.frame = 1

		#add in the vars for if there's a key on base
		self.txk=False
		self.tyk=False
		self.tzk=False
		self.rxk=False
		self.ryk=False
		self.rzk=False
		self.sxk=False
		self.syk=False
		self.szk=False

		self.baseObj = ""

		self.shiftUI()

	def shiftUI(self, *args):
		"""ui for the class"""

		if cmds.window("shiftWin", exists=True):
			cmds.deleteUI("shiftWin")

		self.widgets["win"] = cmds.window("shiftWin", t="zbw_animShift", w=330, h=500)
		self.widgets["mainCLO"] = cmds.columnLayout()


#TO-DO----------------create time options here (all, time slider, range)
		self.widgets["timeRBG"] = cmds.radioButtonGrp(nrb=3, l1="All", l2="Time Slider", l3="Range")
		self.widgets["rangeFFG"] = cmds.floatFieldGrp(l="Start/End Frames", nf=2, v1=0, v2=10)

		cmds.separator(h=5, style="single")

		self.widgets["getBaseBut"]  = cmds.button(l="1. Set Base Object and Frame To Drive Shift", w=330, h=40, bgc=(.6,.8,.6), c=self.getBase)
		self.widgets["baseTFG"] = cmds.textFieldGrp(l="Base Object", cal=((1,"left"), (2,"left")), cw=((1,70),(2,250)), ed=False)
		self.widgets["baseFrameFFG"] = cmds.floatFieldGrp(l="Base Frame", cal = ((1, "left"), (2,"left")), cw=((1,100), (2,50)), pre=2, en=False)

		cmds.separator(h=10)

		self.widgets["valueRCL"] = cmds.rowColumnLayout(nc=3, cw=([1,110],[2,110],[3,110]))
		cmds.text("Orig Values")
		cmds.text("Modified Values")
		cmds.text("Difference Value")

		cmds.separator(style="single", h=5)
		cmds.separator(style="single", h=5)
		cmds.separator(style="single", h=5)

		self.widgets["origTxFFG"] = cmds.floatFieldGrp(l="tx", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["modTxFFG"] = cmds.floatFieldGrp(l="tx", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["difTxFFG"] = cmds.floatFieldGrp(l="tx", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

		self.widgets["origTyFFG"] = cmds.floatFieldGrp(l="ty", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["modTyFFG"] = cmds.floatFieldGrp(l="ty", pre=5, cal=([1,"left"], [2, "left"]),  en=False,cw=([1, 30], [2,75]))
		self.widgets["difTyFFG"] = cmds.floatFieldGrp(l="ty", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

		self.widgets["origTzFFG"] = cmds.floatFieldGrp(l="tz", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["modTzFFG"] = cmds.floatFieldGrp(l="tz", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["difTzFFG"] = cmds.floatFieldGrp(l="tz", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

		cmds.separator(style="single", h=5)
		cmds.separator(style="single", h=5)
		cmds.separator(style="single", h=5)

		self.widgets["origRxFFG"] = cmds.floatFieldGrp(l="rx", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["modRxFFG"] = cmds.floatFieldGrp(l="rx", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["difRxFFG"] = cmds.floatFieldGrp(l="rx", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

		self.widgets["origRyFFG"] = cmds.floatFieldGrp(l="ry", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["modRyFFG"] = cmds.floatFieldGrp(l="ry", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["difRyFFG"] = cmds.floatFieldGrp(l="ry", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

		self.widgets["origRzFFG"] = cmds.floatFieldGrp(l="rz", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["modRzFFG"] = cmds.floatFieldGrp(l="rz", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["difRzFFG"] = cmds.floatFieldGrp(l="rz", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

		cmds.separator(style="single", h=5)
		cmds.separator(style="single", h=5)
		cmds.separator(style="single", h=5)

		self.widgets["origSxFFG"] = cmds.floatFieldGrp(l="sx", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["modSxFFG"] = cmds.floatFieldGrp(l="sx", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["difSxFFG"] = cmds.floatFieldGrp(l="sx", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

		self.widgets["origSyFFG"] = cmds.floatFieldGrp(l="sy", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["modSyFFG"] = cmds.floatFieldGrp(l="sy", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["difSyFFG"] = cmds.floatFieldGrp(l="sy", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

		self.widgets["origSzFFG"] = cmds.floatFieldGrp(l="sz", pre=5, cal=([1,"left"], [2, "left"]), en=False, cw=([1, 30], [2,75]))
		self.widgets["modSzFFG"] = cmds.floatFieldGrp(l="sz", pre=5, cal=([1,"left"], [2, "left"]), en=False,cw=([1, 30], [2,75]))
		self.widgets["difSzFFG"] = cmds.floatFieldGrp(l="sz", pre=5, cal=([1,"left"], [2, "left"]), cw=([1, 30], [2,75]))

		cmds.separator(style="single", h=5)
		cmds.separator(style="single", h=5)
		cmds.separator(style="single", h=5)

		cmds.setParent(self.widgets["mainCLO"])

		#button to capture and calculate changes to the anim curves
		self.widgets["captureBut"] = cmds.button(l="2. Calculate and Capture Changed Values", w=330, h=30, bgc=(.8,.8,.6), c=self.captureChanges)

		cmds.separator(style="single", h=5)

		self.widgets["moveBut"] = cmds.button(l="3. Shift the Anim Curves for Selected Objects!", w=330, h=30, bgc=(.6,.6,.8), c=self.shiftAnim)

		cmds.separator(style="single", h=10)

		#2 column layout to spread these two buttons
		self.widgets["bottomButtonRCL"] = cmds.rowColumnLayout(nc=2, w=330, cw=((1,250), (2,80)))
		self.widgets["clearButton"] = cmds.button(l="Clear All Values!", w=250, h=30, bgc=(.8,.6,.6), c=self.clearAll)
		self.widgets["restoreButton"] = cmds.button(l="Restore Base", w=80, h=30, bgc=(.8,.5,.5), c=self.restoreBase)
		cmds.showWindow(self.widgets["win"])
		cmds.window(self.widgets["win"], e=True, w=330, h=500)


	#####functions#####
	def getBase(self, *args):

		sel = cmds.ls(sl=True, type="transform", l=True)

		if len(sel)>1:
			cmds.warning("You've selected more than one object. Only one object can be the base of the animation shift")
		else:
			obj = sel[0]
			#put sel in the base obj tfg and get the frame
			cmds.textFieldGrp(self.widgets["baseTFG"], e=True, tx=obj)
			self.frame = cmds.currentTime(q=True)
			cmds.floatFieldGrp(self.widgets["baseFrameFFG"], e=True, v1=self.frame)

			btx = cmds.getAttr("%s.tx"%obj)
			bty = cmds.getAttr("%s.ty"%obj)
			btz = cmds.getAttr("%s.tz"%obj)

			brx = cmds.getAttr("%s.rx"%obj)
			bry = cmds.getAttr("%s.ry"%obj)
			brz = cmds.getAttr("%s.rz"%obj)

			bsx = cmds.getAttr("%s.sx"%obj)
			bsy = cmds.getAttr("%s.sy"%obj)
			bsz = cmds.getAttr("%s.sz"%obj)

			cmds.floatFieldGrp(self.widgets["origTxFFG"], e=True, v1=btx)
			cmds.floatFieldGrp(self.widgets["origTyFFG"], e=True, v1=bty)
			cmds.floatFieldGrp(self.widgets["origTzFFG"], e=True, v1=btz)

			cmds.floatFieldGrp(self.widgets["origRxFFG"], e=True, v1=brx)
			cmds.floatFieldGrp(self.widgets["origRyFFG"], e=True, v1=bry)
			cmds.floatFieldGrp(self.widgets["origRzFFG"], e=True, v1=brz)

			cmds.floatFieldGrp(self.widgets["origSxFFG"], e=True, v1=bsx)
			cmds.floatFieldGrp(self.widgets["origSyFFG"], e=True, v1=bsy)
			cmds.floatFieldGrp(self.widgets["origSzFFG"], e=True, v1=bsz)

			if cmds.keyframe("%s.tx"%(obj), q=True, t=(self.frame, self.frame)):
				self.txk = True
			if cmds.keyframe("%s.ty"%(obj), q=True, t=(self.frame, self.frame)):
				self.tyk = True
			if cmds.keyframe("%s.tz"%obj, q=True, t=(self.frame, self.frame)):
				self.tzk = True

			if cmds.keyframe("%s.rx"%(obj), q=True, t=(self.frame, self.frame)):
				self.rxk = True
			if cmds.keyframe("%s.ry"%(obj), q=True, t=(self.frame, self.frame)):
				self.ryk = True
			if cmds.keyframe("%s.rz"%obj, q=True, t=(self.frame, self.frame)):
				self.rzk = True

			if cmds.keyframe("%s.sx"%(obj), q=True, t=(self.frame, self.frame)):
				self.sxk = True
			if cmds.keyframe("%s.sy"%(obj), q=True, t=(self.frame, self.frame)):
				self.syk = True
			if cmds.keyframe("%s.sz"%obj, q=True, t=(self.frame, self.frame)):
				self.szk = True

			#catch the base object  and frame for later use
			self.baseObj = obj

	def captureChanges(self, *args):
		"""method to capture value changes"""
#TO-DO----------------check to make sure there is somethign in the base object
		obj = cmds.textFieldGrp(self.widgets["baseTFG"], q=True, tx=True)
		frame = cmds.floatFieldGrp(self.widgets["baseFrameFFG"], q=True, v1=True)
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

		cmds.floatFieldGrp(self.widgets["modTxFFG"], e=True, v1=mtx)
		cmds.floatFieldGrp(self.widgets["modTyFFG"], e=True, v1=mty)
		cmds.floatFieldGrp(self.widgets["modTzFFG"], e=True, v1=mtz)

		cmds.floatFieldGrp(self.widgets["modRxFFG"], e=True, v1=mrx)
		cmds.floatFieldGrp(self.widgets["modRyFFG"], e=True, v1=mry)
		cmds.floatFieldGrp(self.widgets["modRzFFG"], e=True, v1=mrz)

		cmds.floatFieldGrp(self.widgets["modSxFFG"], e=True, v1=msx)
		cmds.floatFieldGrp(self.widgets["modSyFFG"], e=True, v1=msy)
		cmds.floatFieldGrp(self.widgets["modSzFFG"], e=True, v1=msz)

		#get orig values
		otx = cmds.floatFieldGrp(self.widgets["origTxFFG"], q=True, v1=True)
		oty = cmds.floatFieldGrp(self.widgets["origTyFFG"], q=True, v1=True)
		otz = cmds.floatFieldGrp(self.widgets["origTzFFG"], q=True, v1=True)

		orx = cmds.floatFieldGrp(self.widgets["origRxFFG"], q=True, v1=True)
		ory = cmds.floatFieldGrp(self.widgets["origRyFFG"], q=True, v1=True)
		orz = cmds.floatFieldGrp(self.widgets["origRzFFG"], q=True, v1=True)

		osx = cmds.floatFieldGrp(self.widgets["origSxFFG"], q=True, v1=True)
		osy = cmds.floatFieldGrp(self.widgets["origSyFFG"], q=True, v1=True)
		osz = cmds.floatFieldGrp(self.widgets["origSzFFG"], q=True, v1=True)

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

		cmds.floatFieldGrp(self.widgets["difTxFFG"], e=True, v1=dtx)
		cmds.floatFieldGrp(self.widgets["difTyFFG"], e=True, v1=dty)
		cmds.floatFieldGrp(self.widgets["difTzFFG"], e=True, v1=dtz)

		cmds.floatFieldGrp(self.widgets["difRxFFG"], e=True, v1=drx)
		cmds.floatFieldGrp(self.widgets["difRyFFG"], e=True, v1=dry)
		cmds.floatFieldGrp(self.widgets["difRzFFG"], e=True, v1=drz)

		cmds.floatFieldGrp(self.widgets["difSxFFG"], e=True, v1=dsx)
		cmds.floatFieldGrp(self.widgets["difSyFFG"], e=True, v1=dsy)
		cmds.floatFieldGrp(self.widgets["difSzFFG"], e=True, v1=dsz)


	def shiftAnim(self, *args):
		"""method that does the shifting"""

#TO-DO----------------call the frame range option
		#actually do this with a separate function
		self.startF = 0
		self.endF = 1

		base = cmds.textFieldGrp(self.widgets["baseTFG"], q=True, tx=True)

		#get vals of changes for each
		dtx = cmds.floatFieldGrp(self.widgets["difTxFFG"], q=True, v1=True)
		dty = cmds.floatFieldGrp(self.widgets["difTyFFG"], q=True, v1=True)
		dtz = cmds.floatFieldGrp(self.widgets["difTzFFG"], q=True, v1=True)

		drx = cmds.floatFieldGrp(self.widgets["difRxFFG"], q=True, v1=True)
		dry = cmds.floatFieldGrp(self.widgets["difRyFFG"], q=True, v1=True)
		drz = cmds.floatFieldGrp(self.widgets["difRzFFG"], q=True, v1=True)

		dsx = cmds.floatFieldGrp(self.widgets["difSxFFG"], q=True, v1=True)
		dsy = cmds.floatFieldGrp(self.widgets["difSyFFG"], q=True, v1=True)
		dsz = cmds.floatFieldGrp(self.widgets["difSzFFG"], q=True, v1=True)

		sel = cmds.ls(sl=True, type="transform", l=True)

		if sel:
			for obj in sel:
				cmds.keyframe(obj, at=("tx"), r=True, vc=dtx)
				cmds.keyframe(obj, at=("ty"), r=True, vc=dty)
				cmds.keyframe(obj, at=("tz"), r=True, vc=dtz)

				cmds.keyframe(obj, at=("rx"), r=True, vc=drx)
				cmds.keyframe(obj, at=("ry"), r=True, vc=dry)
				cmds.keyframe(obj, at=("rz"), r=True, vc=drz)

				cmds.keyframe(obj, at=("sx"), r=True, vc=dsx)
				cmds.keyframe(obj, at=("sy"), r=True, vc=dsy)
				cmds.keyframe(obj, at=("sz"), r=True, vc=dsz)

				if obj==base:
					if self.txk:
						#offset the value BACK at self.frame
						cmds.keyframe(obj, at="tx", r=True, vc=-self.dtx, t=(self.frame, self.frame))
					else:
						#delete the key at self.frame if it exists
						cmds.cutKey(obj, at="tx", t=(self.frame, self.frame), cl=True)
					if self.tyk:
						cmds.keyframe(obj, at="ty", r=True, vc=-self.dty, t=(self.frame, self.frame))
					else:
						cmds.cutKey(obj, at="ty", t=(self.frame, self.frame), cl=True)
					if self.tzk:
						cmds.keyframe(obj, at="tz", r=True, vc=-self.dtz, t=(self.frame, self.frame))
					else:
						cmds.cutKey(obj, at="tz", t=(self.frame, self.frame), cl=True)

					if self.rxk:
						cmds.keyframe(obj, at="rx", r=True, vc=-self.drx, t=(self.frame, self.frame))
					else:
						cmds.cutKey(obj, at="rx", t=(self.frame, self.frame), cl=True)
					if self.ryk:
						cmds.keyframe(obj, at="ry", r=True, vc=-self.dry, t=(self.frame, self.frame))
					else:
						cmds.cutKey(obj, at="ry", t=(self.frame, self.frame), cl=True)
					if self.rzk:
						cmds.keyframe(obj, at="rz", r=True, vc=-self.drz, t=(self.frame, self.frame))
					else:
						cmds.cutKey(obj, at="rz", t=(self.frame, self.frame), cl=True)

					if self.sxk:
						cmds.keyframe(obj, at="sx", r=True, vc=-self.dsx, t=(self.frame, self.frame))
					else:
						cmds.cutKey(obj, at="sx", t=(self.frame, self.frame), cl=True)
					if self.syk:
						cmds.keyframe(obj, at="sy", r=True, vc=-self.dsy, t=(self.frame, self.frame))
					else:
						cmds.cutKey(obj, at="sy", t=(self.frame, self.frame), cl=True)
					if self.szk:
						cmds.keyframe(obj, at="sz", r=True, vc=-self.dsz, t=(self.frame, self.frame))
					else:
						cmds.cutKey(obj, at="sz", t=(self.frame, self.frame), cl=True)


		else:
			cmds.warning("You've unselected stuff and you need some selections to shift!")

		#clear base object (so we don't double up on keyframe corrections)
		cmds.textFieldGrp(self.widgets["baseTFG"], e=True, tx="")

	def clearAll(self, *args):
		"""clears all the fields"""
		fieldNames = ["origTxFFG", "origTyFFG", "origTzFFG", "origSxFFG", "origSyFFG", "origSzFFG", "origRxFFG", "origRyFFG", "origRzFFG", "modTxFFG", "modTyFFG", "modTzFFG", "modRxFFG", "modRyFFG", "modRzFFG", "modSxFFG", "modSyFFG", "modSzFFG", "difTxFFG", "difTyFFG", "difTzFFG", "difRxFFG", "difRyFFG", "difRzFFG", "difSxFFG", "difSyFFG", "difSzFFG"]
		cmds.textFieldGrp(self.widgets["baseTFG"], e=True, tx="")
		for field in fieldNames:
			cmds.floatFieldGrp(self.widgets[field], e=True, v1=0)
		cmds.floatFieldGrp(self.widgets["baseFrameFFG"], e=True, v1=0)


	def restoreBase(self, *args):
		"""restores the base obj to the text field"""

		cmds.textFieldGrp(self.widgets["baseTFG"], e=True, tx=self.baseObj)
		cmds.floatFieldGrp(self.widgets["baseFrameFFG"], e=True, v1=self.frame)

#TO-DO----------------get frame ranges from UI, switch out options for enabled frame range
	def enableRange(self, *args):
		pass


	def getRange(self, *args):
		"""this finds the frame range and returns the StartFrame and EndFrame"""
		pass

def animShift(*args):
	thisShift = AnimShift()