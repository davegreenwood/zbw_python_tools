# to zero out the scales of an object
import maya.cmds as cmds

def zeroScale(*args):
	#first grab the objects in question
	sel = cmds.ls(sl=True, l=True)

	for obj in sel:
		#grab the rots and transls
		rots = cmds.getAttr("%s.rotate"%obj)[0]
		trans = cmds.getAttr("%s.translate"%obj)[0]
		print rots
		#zero the rots and transls



