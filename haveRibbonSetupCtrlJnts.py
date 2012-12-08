import maya.cmds as cmds
import zbw_rig as rig

#TO-DO----------------already have ribbon with shitton of joints. Deleted control structure. Create a chain for the master controls

cmds.select(hi=True)
sel = cmds.ls(sl=True)
ctrlList = []
groupList = []

for x in sel:
	if (cmds.listRelatives(x, p=True)):
		cmds.parent(x, w=True)
		#could rename joint here
	ctrl = rig.createControl("%s_CTRL"%x, "cube", "x", "red")
	ctrlList.append(ctrl)
	group = rig.groupOrient(x, ctrl)
	groupList.append(group)
	cmds.parent(x, ctrl)
	
	
for x in range(len(ctrlList)-1, 0, -1):
	cmds.parent(groupList[x], ctrlList[x-1])
	
#TO-DO----------------for ribbon spine with controls, parent the group below to the control (joints are parented under the control). Then you can put a "local" control onto the joint to do the up/down stuff for each control