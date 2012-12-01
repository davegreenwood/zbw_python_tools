import maya.OpenMaya as OpenMaya
import maya.cmds as cmds

def softSelection():
    #Grab the soft selection
    selection = OpenMaya.MSelectionList()
    softSelection = OpenMaya.MRichSelection()
    OpenMaya.MGlobal.getRichSelection(softSelection)
    softSelection.getSelection(selection)

    dagPath = OpenMaya.MDagPath()
    component = OpenMaya.MObject()

    # Filter Defeats the purpose of the else statement
    iter = OpenMaya.MItSelectionList( selection,OpenMaya.MFn.kMeshVertComponent )
    elements, weights = [], []
    while not iter.isDone():
        iter.getDagPath( dagPath, component )
        dagPath.pop() #Grab the parent of the shape node
        node = dagPath.fullPathName()
        fnComp = OpenMaya.MFnSingleIndexedComponent(component)
        getWeight = lambda i: fnComp.weight(i).influence() if fnComp.hasWeights() else 1.0

        for i in range(fnComp.elementCount()):
            elements.append('%s.vtx[%i]' % (node, fnComp.element(i)))
            weights.append(getWeight(i))
        iter.next()

    return elements, weights
elements,weights = softSelection()

print elements
print weights

#select each of the points from the list and create a cluster
cmds.select(cl=True)
for elem in elements:
    cmds.select(elem, add=True)

clus = cmds.cluster(relative=True, name="thisCluster")

for i in range(len(elements)):
    element = elements[i]
    value = weights[i]
    #percent -v 0.5 thisCluster pSphere1.vtx[241] ;
    cmds.percent(clus[0], element,  v=value, )


# create a loc and move it to the position of the cluster. create closest point on surface or mesh node. Add the base geos mesh or surface to the input, then add the transforms xform matrix to the input matrix, then use the pos of the loc as the position of closestOnMesh, then create group and move that to the closest point on surface (deal with the normals?). Then create a control at the origin and put that at the group's position (group orient?). Delete all the other shit adn then put the clusters weighted node as the control and move from origin back to 000 on the cluster.