"""
Created on Fri July 22 2022

@author: Simon Carmona @Vinterdragen

Disables the sRGB property of a texture.

Selected assets must be textures.

This is ideal in the case of masks and greyscale maps
embedded inside the RGBA channels, so the textures can
work properly as linear data.

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
        texture.set_editor_property("srgb", False)
        
        # Print te result of each texture asset
        unreal.log("Name: {} - sRGB = {}".format(texture.get_fname(), texture.get_editor_property("srgb")))
        
    # Tell the user that it's over :P
    unreal.log("sRGB property has been successfully removed...")
else :
    unreal.log("No texture assets selected, please select some textures... ".format(lmr))