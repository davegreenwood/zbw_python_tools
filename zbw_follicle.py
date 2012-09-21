#create a follicle on the specified uv location
import maya.cmds as cmds
import maya.mel as mel


def zbw_follicle(surface="none", u=0.0, v=0.0, *args):
	#get the surface
	#get the uv positions

	#createHair 1 6 2 0 0 0 0 5 0 2 1 1; example with 6 follicles
	#hairSystem1OutputCurves - name of hair curve group

	# sel = cmds.ls(sl=True)[0]
	# shape = cmds.listRelatives(sel, shapes=True)
	# print shape

	# type = cmds.objectType(shape)
	# print type

	# follList = cmds.ls(type="follicle")
	# print follList

	# string $nur


	# string $poly[] = `ls -sl -dag -type mesh`;
	# string $fol = `createNode follicle`;
	# string $folTrans[] = `listRelatives -parent $fol`;
	# connectAttr -f ($poly[0]+".worldMatrix") ($fol+".inputWorldMatrix");
	# connectAttr -f ($poly[0]+".outMesh") ($fol + ".inputMesh");
	# connectAttr -f ($fol+".outTranslate") ($folTrans[0] + ".translate");
	# connectAttr -f ($fol+".outRotate") ($folTrans[0] + ".rotate");
	# setAttr ($fol+".parameterU") 0.75;
	# setAttr ($fol+".parameterV") 0.75;

#one way to do it
# {
# 	string $follicle = `createNode follicle`;
# 	string $tforms[] = `listTransforms $follicle`;
# 	string $follicleDag = $tforms[0];

	
# 	connectAttr ($surface + ".worldMatrix[0]") ($follicle + ".inputWorldMatrix");
# 	string $nType = `nodeType $surface`;
# 	if( "nurbsSurface" == $nType ){ 
# 		connectAttr ($surface + ".local") ($follicle + ".inputSurface");
# 	} else {
# 		connectAttr ($surface + ".outMesh") ($follicle + ".inputMesh");
# 	}
# 	connectAttr ($follicle + ".outTranslate") ($follicleDag + ".translate");
# 	connectAttr ($follicle + ".outRotate") ($follicleDag + ".rotate");
# 	setAttr -lock true  ($follicleDag + ".translate");
# 	setAttr -lock true  ($follicleDag + ".rotate");
# 	setAttr ($follicle + ".parameterU") $u;
# 	setAttr ($follicle + ".parameterV") $v;
	
# 	//parent -addObject -shape $obj $follicleDag;
# 	parent $obj $follicleDag;
# }




	pass
