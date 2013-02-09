#
#to run. . .
#import zbw_clipPlanes as cp 
#cp.clipPlanes()
#
import maya.cmds as cmds

def setClipUI(*args):
    if cmds.window("SCPwin", exists=True):
        cmds.deleteUI("SCPwin")
    cmds.window("SCPwin", t="Set Clip Planes", w=200, h=100)
    cmds.columnLayout("colLO")
    cmds.checkBox("allCB", l="All Cameras? (vs. selected)", v=True)
    cmds.floatFieldGrp("nearFFG", l="nearClip", v1=1, cal=([1,"left"], [2,"left"]), cw=([1,50], [2,150]))
    cmds.floatFieldGrp("farFFG", l="farClip", v1=100000, cal=([1,"left"], [2,"left"]), cw=([1,50], [2,150]))
    cmds.button("button", l="Set Clip Planes", h=50, w=250, bgc=(.8, .6,.6), c=setPlanes)
    
    cmds.showWindow("SCPwin")
    cmds.window("SCPwin", e=True, w=200, h=100)
    
    
def setPlanes(*args):
    all = cmds.checkBox("allCB", q=True, v=True)
    far = cmds.floatFieldGrp("farFFG", q=True, v1=True)
    near = cmds.floatFieldGrp("nearFFG", q=True, v1=True)
    
    cams = []
    if all:
        cams.extend(cmds.ls(type="camera"))
    if not all:
        transf = cmds.ls(sl=True, type="transform")
        for each in transf:
            shape = cmds.listRelatives(each, s=True)
            if shape:
                if cmds.objectType(shape) == "camera":
                    cams.extend(shape)
    #for each, set shape.farClipPlane 100000
    if cams:
        print cams
        for cam in cams:
            try:
                cmds.setAttr("%s.farClipPlane"%cam, far)
                cmds.setAttr("%s.nearClipPlane"%cam, near)

            except:
                cmds.warning("Couldn't change the farClipPlane of %s"%cam)
    
    
def setClipPlanes(*args):
    setClipUI()
