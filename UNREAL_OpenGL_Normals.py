"""
Created on Fri July 22 2022

@author: Simon Carmona @Vinterdragen

Sets up OpenGL normal maps to work correctly inside Unreal.

Selected assets must be normal map textures.

Unreal Engine uses DirectX normal maps... In order tomake OpenGL generated normals
the green channel has to be flipped.

"""

import unreal

# Create unreal class instances
editor_util = unreal.EditorUtilityLibrary()
system_lib = unreal.SystemLibrary()

# Get the selected assets
selected_assets = editor_util.get_selected_assets()
num_assets = len(selected_assets)

# Checks if there's anything selected
if num_assets > 0 :

    # Applies the setting for each selected texture
    for texture in selected_assets:
        texture.set_editor_property("flip_green_channel", True)

        # Print te result of each texture asset
        unreal.log("Name: {} G channel is now flipped".format(texture.get_fname()))

    # Tell the user that it's over :P
    unreal.log("Selected OpenGL normal maps have been set to work properly.")

else :
    unreal.log("No texture assets selected, please select some textures... ".format(lmr))