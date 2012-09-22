import maya.cmds as cmds

#-------multiple selection and average uv position?
#-------grab an edge and convert to 2 verts and get average. . .

#get vertex
vertex = cmds.ls(sl=True, fl=True)

#convert vertex to uvs
uvs = cmds.polyListComponentConversion(fv=True, tuv=True)
#flatten the uv to list and grab first (cuz verts can be multiple uv's)
uv = cmds.ls(uv, fl=True)[0]

#select our uv
cmds.select(uv, r=True)
#convert the uv index to u and v values
uvVal = cmds.polyEditUV(q=True)
cmds.select(vertex)
return(uvVal)