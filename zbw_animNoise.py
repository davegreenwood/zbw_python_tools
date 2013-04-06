#TO-DO----------------MAKE ENTIRE THING A MODULE
#TO-DO----------------better UI
#TO-DO----------------

import maya.cmds as cmds
import random

def zbw_animNoiseRange(*args):
    onOff=cmds.checkBoxGrp('zbw_animNoiseTimeOn', q=True, value1=True)
    if not onOff:
        cmds.floatFieldGrp('zbw_animNoiseFrameRange', e=True, en=1)
    else:
        cmds.floatFieldGrp('zbw_animNoiseFrameRange', e=True, en=0)

def zbw_animNoiseRandom(*args):
    onOff=cmds.checkBoxGrp('zbw_animNoiseRandom', q=True, value1=True)
    if not onOff:
        cmds.floatFieldGrp('zbw_animNoiseRandFreq', e=True, en=0)
    else:
        cmds.floatFieldGrp('zbw_animNoiseRandFreq', e=True, en=1)


if (cmds.window('zbw_animNoiseUI', exists=True)):
    cmds.deleteUI('zbw_animNoiseUI', window=True)
    cmds.windowPref('zbw_animNoiseUI', remove=True)
window=cmds.window('zbw_animNoiseUI', widthHeight=(350,200), title='zbw_animNoise')
cmds.columnLayout(cal='center')
cmds.floatFieldGrp('zbw_animNoiseAmp', cal=(1, 'left'), nf=2, label="set Min/Max Amp", value1=-1.0, value2=1.0)
#add gradient?
cmds.floatFieldGrp('zbw_animNoiseFreq', cal=(1,'left'), label='frequency(frames)', value1=5)
#checkbox for random freq
cmds.checkBoxGrp('zbw_animNoiseRandom', cal=(1,'left'), cw=(1, 175),label='random frequency on', value1=0, cc=zbw_animNoiseRandom)
cmds.floatFieldGrp('zbw_animNoiseRandFreq', label='random freq (frames)', value1=1, en=0)
#checkbox for avoid keys
cmds.checkBoxGrp('zbw_animNoiseAvoid', cal=(1,'left'), cw=(1, 175),label='buffer existing keys (by freq)', value1=0)
#radiobutton group for tangents
#checkbox for timeline range
cmds.checkBoxGrp('zbw_animNoiseTimeOn', cal=(1,'left'), cw=(1, 175),label='use timeline start/end', value1=1, cc=zbw_animNoiseRange)
#floatFieldGrp for range
cmds.floatFieldGrp('zbw_animNoiseFrameRange', nf=2, label='start/end frames', value1=1, value2=10, en=0)
cmds.text("")
cmds.button('zbw_animNoiseGo', label='add Random', width=75, command=checkIt)

cmds.showWindow(window)

###MAKE ALL THIS A FUNCTION!!!!
#figure out GUI
#DONE,BUT COULD BE MORE GENERAL -figure out how to grab attrs from channel box (in Mel use "global string $gchannelBox")

#DUMMYCHECK THAT OBJECTS ARE SELECTED
channels = cmds.channelBox ('mainChannelBox', query=True,selectedMainAttributes=True)

#DUMMYCHECK THAT ATTRS ARE SELECTED
obj = []
obj = cmds.ls(selection=True)
#get frequency value
freq=cmds.floatFieldGrp('zbw_animNoiseFreq', q=True, value=True)
#should freq value have randomness?
randFreq = cmds.checkBoxGrp('zbw_animNoiseRandFreq', q=True, value1=True )
addLow = floatFieldGrp('zbw_animNoiseAmp', q=True, value1=True )
addHigh = floatFieldGrp('zbw_animNoiseAmp', q=True, value2=True )
origVal = {}
keyList = []

#deal with range
startF=0
endF=0
if (cmds.checkBoxGrp('zbw_animNoiseTimeOn', q=True, value1=True):
	startF = cmds.playbackOptions (query=True, minTime=True)
	endF = cmds.playbackOptions (query=True, maxTime=True)
else:
	startF = cmds.floatFieldGrp('zbw_animNoiseFrameRange', q=True, value1=True)
	endF = cmds.floatFieldGrp('zbw_animNoiseFrameRange', q=True, value2=True)

#MAKE SURE TO SET AUTOKEY FOR ATTRS SELECTED

#CHANGE BELOW TO STEP THROUGH BY FRAME/RAND AND KEY VALUES BY (RAND FUNC)
for me in obj:
	for this in channels:
		channel = me + '.' + this
		#create keyList of frames for keys on this attr
		#DUMMY CHECK THAT KEYS EXIST
		keyList=cmds.keyframe(me, query=True, time=(startF,endF),attribute=this)
		#to create dictionary of orig values to access in a sec
		for i in range(startF,endF,freq):
			cmds.currentTime(i,edit=True)
			origVal[i] = cmds.getAttr(channel)
		#to create rand number and add that to orig value and setKey
		for i in range(startF,endF,freq):
			cmds.currentTime(i, edit=True)
			addVal = float(random.uniform(addLow,addHigh))
			oldVal = origVal[i]
			newVal = (oldVal + addVal)
			disCheck = []
			#check that the new keys aren't going to be within freq of existing keys
			#THIS SHOULD ONLY BE OPTION? "PROTECT KEYS"
			for key in keyList:
				nowF = cmds.currentTime(query=True)
				distance = abs(key-i)
				if distance<=freq:
					disCheck.append(distance)
			if disCheck:
				pass
			else:
				cmds.setAttr(channel, newVal)

