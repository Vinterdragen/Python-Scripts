import maya.cmds as cmds

"""
Created on Fri July 22 2022

@author: Simon Carmona @Vinterdragen

Sets the correct UV Set to the default UV0 set,
then deletes all the extra unnecesary UV Sets.

"""

# List all selected objects
objectList = cmds.ls( selection = True )

for obj in objectList:
    cmds.polyUVSet(obj, copy=True, nuv='UV0', uvSet='General' )
    cmds.polyUVSet(obj, delete=True, uvSet='UV1')
    cmds.polyUVSet(obj, delete=True, uvSet='UV2')
    cmds.polyUVSet(obj, delete=True, uvSet='UV3')
    cmds.polyUVSet(obj, delete=True, uvSet='General')