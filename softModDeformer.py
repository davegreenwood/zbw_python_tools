import maya.cmds as cmds


# Here's how it goes . . .
# choose a vert (for example)
#TO-DO----------------check for just one vert . . .  
vertex = cmds.ls(sl=True)[0]
obj = vertex.partition(".")[0]

vertPos = cmds.pointPosition(vertex)
print(vertPos)

cmds.select(obj)
# create a soft mod there
cmds.softMod(relative=False, falloffCenter = vertPos, falloffRadius=3.0)
# get position of the softmod
# create a control at the position of the softmod
# connect the pos, rot, scale of the control to the softModHandle
# create an attr on the control for the falloff (and the envelope)
# connect that attr to the softmod falloff radius
# softmod NOT relative
# inherit transforms on softModHandle are "off"

# maybe . . .
# create secondary control under control
# this will drive falloff center attr of the softmod (connect attrs from translate)