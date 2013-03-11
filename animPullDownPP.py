#pull down anim from root (or higher) node, which gets set to 000

import maya.cmds as cmds
import maya.OpenMaya as om
import math
from functools import partial
import maya.mel as mel

#TO-DO----------------revise UI a bit to make it cleaner
#TO_DO----------------save out the selected controls to get them later
#TO-DO----------------figure out how to do step keys (step next)
#TO-DO----------------option to use locs to get ws position and rotation!!!! Or maybe not option, maybe they're all done that way (MAYBE JUST USE RP  IN XFORM INSTEAD OF T)
#TO-DO----------------frame range option? probably not necessary, think of a situation in which you'd need it

#set up UI to enter master controls into list, then enter IK, COG into list
widgets = {}

def animPullDownUI():

    if cmds.window("apdWin",exists=True):
        cmds.deleteUI("apdWin", window=True)
        cmds.windowPref("apdWin", remove=True)

    widgets["win"] = cmds.window("apdWin", t="zbw_pullUpAnim", w=400, h=550)


    widgets["tabLO"] = cmds.tabLayout()
    widgets["mainCLO"] = cmds.columnLayout("SetupControls")

    #----------get frame range?

    #master controls layout
    widgets["zeroFLO"] = cmds.frameLayout("zeroFrameLO", l="Master Controls", w=400, bgc = (0, 0,0), h=200)
    widgets["zeroCLO"] = cmds.columnLayout("zeroColumnLO", w=400)
    cmds.text("Select Master Control Items To Zero Out")
    widgets["zeroBut"] = cmds.button("zeroButton", l="Add Master CTRLs", bgc = (.8,.8,.6), w=400, h=35, c= partial(getControl, "masterTSL"))

    widgets["zeroRCLO"] = cmds.rowColumnLayout("zeroRCLO", nc=2, w=400)
    widgets["zeroClearBut"] = cmds.button("clearZeroButton", l="Clear Selected", w=200, h=30, bgc=(.8,.6,.6), c= partial(clearList, "masterTSL"))
#TO-DO----------------make this a "clear all" button???
    widgets["zeroClearBut"] = cmds.button("moveZeroButton", l="Clear All", w=200, h=30, bgc=(.8,.5,.5), c= partial(clearAll, "zeroTSL"))
    cmds.setParent(widgets["zeroCLO"])
    cmds.separator(h=10)
    widgets["zeroTSL"] = cmds.textScrollList("masterTSL", nr=4, w=400, h=75, ams=True, bgc=(.2, .2, .2))

    #ik items layout
    cmds.setParent(widgets["mainCLO"])
    widgets["IKFLO"] = cmds.frameLayout("IKFrameLO", l = "World Space Controls", w=400, bgc=(0,0,0))
    widgets["IKCLO"] = cmds.columnLayout("IKColumnLO", w=400)
    cmds.text("Select World Space Controls")
    widgets["IKBut"] = cmds.button("IKButton", l="Add World Space CTRLs", w=400, h=35, bgc = (.8,.8,.6), c= partial(getControl, "IKTSL"))

    widgets["IKRCLO"] = cmds.rowColumnLayout("IKRCLO", nc=2, w=400)
    widgets["IKClearSelBut"] = cmds.button("clearIKButton", l="Clear Selected", bgc=(.8,.6,.6), w=200, h=30, c= partial(clearList, "IKTSL"))

    widgets["IKClearAllBut"] = cmds.button("moveIKButton", l="Clear All", w=200, h=30, bgc=(.8,.5,.5), c= partial(clearAll,  "IKTSL"))
    cmds.setParent("IKColumnLO")
    cmds.separator(h=10)
    widgets["IKTSL"] = cmds.textScrollList("IKTSL", nr=10, w=400, h=120, ams=True, bgc=(.2, .2, .2))
    cmds.separator(h=10)


    #doIt button layout
    cmds.setParent(widgets["mainCLO"])
    widgets["doItRCLO"] = cmds.rowColumnLayout("doItLayout", nc=2)
    widgets["doItBut"] = cmds.button("doItButton", l="Pull Animation Down from Master!", w=300, h=50, bgc = (.4,.8,.4), c=pullDownAnim)
    widgets["pullBut"] = cmds.button("pullButton", l="Store IK Controls", w=100, h=50, bgc = (.4,.4,.8))

#TO-DO----------------make the button which passes info into the second tab (which will catch selections for IK controls)

    #create second tab
    cmds.setParent(widgets["tabLO"])
    widgets["storeCLO"] = cmds.columnLayout("Store Control Names")
    widgets["storeFL"] = cmds.frameLayout(l="Stored Control Names", w=400)
    widgets["storeTSL"] = cmds.textScrollList("storeTSL", nr=8, ams=True, bgc=(.2, .2, .2))
    cmds.separator(h=10)
    #back up to clo to setup rclo
    cmds.setParent(widgets["storeCLO"])
    widgets["storeRCL"] = cmds.rowColumnLayout(nc=2)
    widgets["storeClearSelBut"] = cmds.button(l="Clear Selected", bgc = (.8,.6,.6), w=200, h=30)
    widgets["storeClearAllBut"] = cmds.button(l="Clear All", bgc = (.9,.6,.6), w=200, h=30)
    cmds.setParent(widgets["storeCLO"])
    cmds.separator(h=10)
    widgets["storeGetBut"] = cmds.button(l="Add Selected Object Control Name", bgc = (.8,.8,.6), w=400, h=40)
    cmds.separator(h=10)
    widgets["storePullBut"] = cmds.button(l="Find and Push These From Under Selected Mstr", bgc = (.6,.9,.6), w=400, h=40)

    #showWindow
    cmds.showWindow(widgets["win"])

def clearAll(layout, *args):
     """clears the selected text scroll list"""
     pass

def clearList(layout, *args):
    """clears the list of textFields"""
    #get selected items
    sel = cmds.textScrollList(layout, q=True, sii=True)
    #remove selected items
    for item in sel:
        cmds.textScrollList(layout, e=True, rii=True)

def getControl(layout, *args):
    """gets the selected objs and puts them into the assoc. layout"""
    selList = cmds.ls(sl=True, type="transform", l=True)
    if selList:
        cmds.textScrollList(layout, e=True, a=selList)

def getLocalValues(obj, *args):
    """use the matrix to get world space vals, convert to trans and rots"""
    #get values
    #add as key in dict
    obj_values = []

    obj_wRot = cmds.xform(obj, q=True, ws=True, ro=True)
    obj_wTrans = cmds.xform(obj, q=True, ws=True, rp=True)

    for tval in obj_wTrans:
        obj_values.append(tval)
    for rval in obj_wRot:
        obj_values.append(rval)

    return obj_values
    #return (tx, ty, tz, rx, ry, rz)


def pullDownAnim(*args):
    #get master controls
    masters = []
    rawKeys = []
    keyList = []
    worldCtrls = []
    currentTime = mel.eval("currentTime-q;")
    allControls = []
    
    #get list of master ctrls
    mChildren = cmds.textScrollList(widgets["zeroTSL"], q=True, ai=True)
    for thisM in mChildren:
        masters.append(thisM)
        allControls.append(thisM)
        
    #get list of world space objects
    wChildren = cmds.textScrollList(widgets["IKTSL"], q=True, ai=True)
    for thisIK in wChildren:
        worldCtrls.append(thisIK)
        allControls.append(thisIK)
#------------------get keys from secondary controls also. .  . 
    #get full list of keys (keyList)
    for each in allControls:
        #get list of keys for each master
        keys = cmds.keyframe(each, q=True)
        #add keys to rawKeys
        if keys:
            for thisKey in keys:
                rawKeys.append(thisKey)
        #make list from set of list
        keySet = set(rawKeys)
        for skey in keySet:
            keyList.append(skey)
          
    #if no keys, then just add the current time value
    if not rawKeys:
        keyList.append(currentTime)
    
    keyList.sort()
    print keyList

#-------------
    localVals = {}

#for each control, grab the values at that key and store them in a dict, "control":[(vals), (vals)], list of values are at key indices
    for wCtrl in worldCtrls:
        localList = []
        #store these in a dict (obj:(tx, ty, tz, rx, ry, rz))
        for key in keyList:
            mel.eval("currentTime %s;"%key)
            theseVals = getLocalValues(wCtrl)
            localList.append(theseVals)
        localVals[wCtrl] = localList
    print localVals
    
#zero out the master controls
    for key in range(len(keyList)):
        mel.eval("currentTime %s;"%keyList[key])
        for mCtrl in masters:  #should I use setkey?
            cmds.xform(mCtrl, ws=True, t = (0, 0, 0))
            cmds.xform(mCtrl, ws=True, ro = (0, 0, 0))
            cmds.setKeyframe(mCtrl, ott="step", t=keyList[key])
            
        #THEN setKey each control's values to the values in the dict
        for wCtrl in worldCtrls:
            #--------if attr is locked skip it
            cmds.xform(wCtrl, ws=True, t=(localVals[wCtrl][key][0], localVals[wCtrl][key][1], localVals[wCtrl][key][2]))
            cmds.xform(wCtrl, ws=True, ro=(localVals[wCtrl][key][3], localVals[wCtrl][key][4], localVals[wCtrl][key][5]))
            cmds.setKeyframe(wCtrl, ott="step", t=keyList[key])

def animPullDown():
    animPullDownUI()