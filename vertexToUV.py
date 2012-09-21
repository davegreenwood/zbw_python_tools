#get up to mesh data from vertex selection at some point

#get vertex

vertex = cmds.ls(sl=True, fl=True)
print vertex


uv = cmds.polyListComponentConversion(fv=True, tuv=True)
print uv

cmds.select(uv, r=True)
#convert the uv index to u and v values
uvVals = cmds.polyEditUV(q=True)
print uvVals