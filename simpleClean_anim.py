#script to find keys that are doing nothing and delete them

import maya.cmds as cmds

#try to find dead keyframes
sel = cmds.ls(sl=True)

#get timeslider range start
startF = cmds.playbackOptions(query=True, min=True)
endF = cmds.playbackOptions(query=True, max=True)

# loop through objects
for object in sel:
    keyedAttr = []
    # find which attr have keys on them
    keyedAttrRaw = cmds.keyframe(object, q=1, name=1)
    #now fix the "object_" part to "object."
    for oldAttr in keyedAttrRaw:
        newAttr = oldAttr.lstrip((object + "_"))
        keyedAttr.append(newAttr)
        # loop through attrs with keys
    for attr in keyedAttr:
        #loopNum = 0
        for a in range(0,1):
            keyList = []
            keyList = cmds.keyframe(object, query=True, at=attr,time=(startF, endF))
            if (keyList):
                keySize = len(keyList)
                if keySize < 3:
                    if keySize < 2:
                        #pass
                        print ("only one key for " + object + "." + attr)
                        print "cutting " + object + "." + attr
                        currentVal = cmds.getAttr((object+"."+attr), time=keyList[0])
                        cmds.cutKey(object, at=attr, time=(keyList[0],keyList[0]), cl=True)
                        #cmds.setAttr(object, at=attr, time=(keyList[0]), cl=True)
                    else:
                        print "compare two keys for " + attr
                        #check for keep start end options 
                        firstKey = keyList[0]
                        secondKey = keyList[1]
                        firstVal = cmds.keyframe(object, at=attr, query=True, time=(firstKey,firstKey), eval=True)
                        secondVal = cmds.keyframe(object, at=attr, query=True, time=(secondKey,secondKey), eval=True)
                        #add a check in here for keep first keep last
                        if firstVal == secondVal:
                            print "cutting two keys for " + attr
                            cmds.cutKey(object, at=attr, time=(firstKey,secondKey), cl=True)
            
                else:
                    print "here we cycle through the comparisons for " + attr
    
                    for i in range(1,keySize-1):
                        thisKey = keyList[i]
                        prevKey = keyList[i-1]
                        nextKey = keyList[i+1]
                        thisVal = cmds.keyframe(object, at=attr, query=True, time=(thisKey,thisKey), eval=True)
                        prevVal = cmds.keyframe(object, at=attr, query=True, time=(prevKey,prevKey), eval=True)
                        nextVal = cmds.keyframe(object, at=attr, query=True, time=(nextKey,nextKey), eval=True)
                        if (thisVal==prevVal) and (thisVal==nextVal):
                            cmds.cutKey(object, at=attr, time=(thisKey,thisKey), cl=True)   
            else:
                pass
                    

