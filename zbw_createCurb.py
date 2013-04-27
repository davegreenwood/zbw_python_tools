########################
#file: zbw_createCurb.py
#Author: zeth willie
#Contact: zeth@catbuks.com, www.williework.blogspot.com
#Date Modified: 04/27/13
#To Use: type in python window  ""
#Notes/Descriptions: use to create a contiguous poly surface based on an edge selection, etc
########################

import maya.cmds as cmds
import maya.mel as mel

#TO-DO----------------add float field grp to deal with the height fo the bump
#TO-DO----------------rename things to be more generic
#TO-DO----------------add description
#TO-DO----------------option to keep history or not

def curbUI(*args):
    #UI
    if cmds.window("curbWin", exists=True):
        cmds.deleteUI("curbWin")

    cmds.window("curbWin", t="Curb Creator", w=200, h=200)
    cmds.columnLayout("colLO")
    cmds.frameLayout("topFrame", l="Covert Edge", cll=True, bgc=(.2,.2,.2))
    cmds.text("Select poly edge to convert")
    cmds.button("convertBut", l="Convert!", w=200, h=30, bgc=(.7, .8,.7), c=convertEdge)
    cmds.separator(h=5)

    cmds.setParent("colLO")

    cmds.frameLayout("midFrame", l="Create Poly", cll=True, bgc=(.2,.2,.2))
    cmds.text("Select curve")
    cmds.separator(h=5)
    cmds.checkBox("curbCB", l="Positive", v=True)
    cmds.checkBox("bumpCB", l="Add vertical hump?", v=True)
    cmds.floatFieldGrp("curbFFG", l="Curb Width", cal=((1, "left"),(2,"left")), cw=([1,75],[2,50]), v1=150)
    cmds.intFieldGrp("UDivIFG", l="Width Subdivisions", cal=((1, "left"),(2,"left")), cw=([1,75],[2,50]), v1=2)
    cmds.intFieldGrp("VDivIFG", l="Length Subdivisions", cal=((1, "left"),(2,"left")), cw=([1,75],[2,50]), v1=2)

    cmds.separator(h=5)
    cmds.button("curbBut", l="Create Curb", h=40, w=200, bgc=(.7, .8, .7), c = makeCurb)

    cmds.showWindow("curbWin")
    cmds.window("curbWin", e=True, h=150, w=200)


def convertEdge(*args):
    sel = cmds.ls(sl=True, type="transform")
    try:
        mel.eval("polyToCurve -form 2 -degree 3;")
    except:
        cmds.warning("Couldn't complete this operation! Sorry homey.")

def makeCurb(*args):
    #make sure a curve is selected
    sel = cmds.ls(sl=True)[0]
    shape = cmds.listRelatives(sel, s=True)[0]
    type = cmds.objectType(shape)

    if type== "nurbsCurve":
        #offset the curb
        distance = cmds.floatFieldGrp("curbFFG", q=True, v1=True)
        bump = cmds.checkBox("bumpCB", q=True, v=True)
        pos = cmds.checkBox("curbCB", q=True, v=True)
        if pos == 0:
            dist = distance * -1
        else:
            dist = distance
        U = cmds.intFieldGrp("UDivIFG", q=True, v1=True)
        V = cmds.intFieldGrp("VDivIFG", q=True, v1=True)

        outCurve = cmds.offsetCurve(sel, d=dist, n="outerCurb")
        midCurve = cmds.offsetCurve(sel, d=dist/2, n="midCurb")
        if bump:
            cmds.xform(midCurve, ws=True, r=True, t=(0,5,0))

        cmds.select(cl=True)

        lofted = cmds.loft(sel, midCurve, outCurve)[0]

        poly = cmds.nurbsToPoly(lofted, pt=1, ch=False, f=2, un=U, vn=V)[0]

        curbGrp = cmds.group(empty=True, n="curb_grp")

        cmds.rename(poly, "polyCurb")

        cmds.parent(lofted, outCurve, midCurve, sel, curbGrp)

        cmds.setAttr("%s.v"%curbGrp, 0)
    else:
        cmds.warning("You need to select a curve!")
def createCurb():
    curbUI()