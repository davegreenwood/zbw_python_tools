#gets selected obj and uses a slider to scale it's components, leaving the transform clean

import maya.cmds as cmds



def shapeScaleUI():
    if (cmds.window("shapeScaleWin", exists=True)):
        cmds.deleteUI("shapeScaleWin", window=True)
        #cmds.winPref("shapeScaleWin", remove=True)

    cmds.window("shapeScaleWin", w=400, h=100)

    cmds.columnLayout("mainCLO", w=400, h=100)

    cmds.floatSliderGrp("slider", f=False, l="scale", min=0.01, max=2, pre=3, v=1, adj=3, cal=([1, "left"], [2, "left"], [3, "left"]), cw=([1, 75], [2,325]), cc= shapeScaleExecute)

    cmds.separator(h=20)

    cmds.rowColumnLayout("scaleRCLO", nc=2, w=400)
    cmds.floatFieldGrp("scalePer", v1=100, pre= 3, l="Scale %", en1=False, w=200, cw=([1,75],[2,75]), cal=([1,"left"], [2,"left"])) #, cc=manualScale
    cmds.button("scaleReset", w= 200, c=resetScale)

    cmds.setParent("mainCLO")
    cmds.separator(h=20)

    cmds.text("choose the transform of the object you want then enter values or")
    cmds.text("use the slider to edit the scale of the components (not the xform)")


    cmds.showWindow("shapeScaleWin")
    cmds.window("shapeScaleWin", e=True, w=400, h=100)

def resetScale(*args):
    cmds.floatFieldGrp("scalePer", e=True, v1=100)
    pass

def manualScale(*args):
    #get value from field
    scalePer = cmds.floatFieldGrp("scalePer", q=True, v1=True)
    scaleVal = scalePer/100
    #scaleShapes
    sel = cmds.ls(sl=True, type="transform")
    for obj in sel:
        #decide on object type

        cmds.select(cl=True)
        #get the components
        cvs = cmds.select((obj + ".cv[*]"))
        cmds.scale(scaleVal, scaleVal, scaleVal)

    #clear and reselect all
    cmds.select(cl=True)
    cmds.select(sel)

    pass

def shapeScaleExecute(*args):
    """takes the components of the selected obj and scales them according the slider"""

    oldScale = cmds.floatFieldGrp("scalePer", q=True, v1=True)

    #get the selected obj
    sel = cmds.ls(sl=True, type="transform")

    #get the value from the slider
    scaleVal = cmds.floatSliderGrp("slider", q=True, v=True)

    for obj in sel:
        #decide on object type

        cmds.select(cl=True)
        #get the components
        cvs = cmds.select((obj + ".cv[*]"))
        cmds.scale(scaleVal, scaleVal, scaleVal)
        #fix scale adjuster
        newScale = oldScale * scaleVal
        cmds.floatFieldGrp("scalePer", e=True, v1=newScale)


    #reset slider to 1, so we don't stack scalings
    cmds.floatSliderGrp("slider", e=True, v=1)

    #clear and reselect all
    cmds.select(cl=True)
    cmds.select(sel)

def shapeScale():
    shapeScaleUI()

