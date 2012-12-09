#TO-DO----------------also think about selecting all the cards. . . for each, run closestPointOnSurface function for the dummy geo, create a follicle at the closest point(UV) and parent it to that. . . .
import maya.cmds as cmds

sel = cmds.ls(sl=True)
#get all the cards (could be groups)
cards = sel[1:]

#get the proxy geo
shell = sel[0]

#for each card (or group) get the nearest point on surface of proxy
for card in cards:
	#use closest point on surface to get the uv
	
	#from that uv, create a follicle on the proxy

	#constrain the card to the follicle


