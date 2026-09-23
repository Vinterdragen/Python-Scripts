bl_info = {
    "name": "Mixamo to UE5 Bone Renamer",
    "author": "Simon Carmona. 2026.",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > TA Tools",
    "description": "Renames Mixamo's bones to the Unreal Engine 5 standard. Non-standard bones keep untouched, so make sure to delete those after if you don't want them.",
    "category": "Rigging",
}

import bpy

class RIGGING_OT_mixamo_to_ue5(bpy.types.Operator):
    """Renames Mixamo's bones to the Unreal Engine 5 standard."""
    bl_idname = "rigging.mixamo_to_ue5"
    bl_label = "Rename Mixamo to UE5"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "Select an active Armature")
            return {'CANCELLED'}

        bone_mapping = {
            "Hips": "pelvis", "Spine": "spine_01", "Spine1": "spine_02", "Spine2": "spine_03",
            "Neck": "neck_01", "Head": "head",
            "LeftShoulder": "clavicle_l", "LeftArm": "upperarm_l", "LeftForeArm": "lowerarm_l", "LeftHand": "hand_l",
            "RightShoulder": "clavicle_r", "RightArm": "upperarm_r", "RightForeArm": "lowerarm_r", "RightHand": "hand_r",
            "LeftUpLeg": "thigh_l", "LeftLeg": "calf_l", "LeftFoot": "foot_l", "LeftToeBase": "ball_l",
            "RightUpLeg": "thigh_r", "RightLeg": "calf_r", "RightFoot": "foot_r", "RightToeBase": "ball_r",
            
            "LeftHandThumb1": "thumb_01_l", "LeftHandThumb2": "thumb_02_l", "LeftHandThumb3": "thumb_03_l",
            "LeftHandIndex1": "index_01_l", "LeftHandIndex2": "index_02_l", "LeftHandIndex3": "index_03_l",
            "LeftHandMiddle1": "middle_01_l", "LeftHandMiddle2": "middle_02_l", "LeftHandMiddle3": "middle_03_l",
            "LeftHandRing1": "ring_01_l", "LeftHandRing2": "ring_02_l", "LeftHandRing3": "ring_03_l",
            "LeftHandPinky1": "pinky_01_l", "LeftHandPinky2": "pinky_02_l", "LeftHandPinky3": "pinky_03_l",
            
            "RightHandThumb1": "thumb_01_r", "RightHandThumb2": "thumb_02_r", "RightHandThumb3": "thumb_03_r",
            "RightHandIndex1": "index_01_r", "RightHandIndex2": "index_02_r", "RightHandIndex3": "index_03_r",
            "RightHandMiddle1": "middle_01_r", "RightHandMiddle2": "middle_02_r", "RightHandMiddle3": "middle_03_r",
            "RightHandRing1": "ring_01_r", "RightHandRing2": "ring_02_r", "RightHandRing3": "ring_03_r",
            "RightHandPinky1": "pinky_01_r", "RightHandPinky2": "pinky_02_r", "RightHandPinky3": "pinky_03_r"
        }

        renamed_count = 0
        for bone in obj.data.bones:
            # Limpiar prefijo 'mixamorig:' si existe
            base_name = bone.name.replace("mixamorig:", "")
            
            if base_name in bone_mapping:
                bone.name = bone_mapping[base_name]
                renamed_count += 1

        self.report({'INFO'}, f"Huesos renombrados: {renamed_count}")
        return {'FINISHED'}

class VIEW3D_PT_ta_tools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TA Tools'
    bl_label = "Rigging Pipeline"

    def draw(self, context):
        layout = self.layout
        layout.operator("rigging.mixamo_to_ue5", icon='BONE_DATA')

def register():
    bpy.utils.register_class(RIGGING_OT_mixamo_to_ue5)
    bpy.utils.register_class(VIEW3D_PT_ta_tools)

def unregister():
    bpy.utils.unregister_class(RIGGING_OT_mixamo_to_ue5)
    bpy.utils.unregister_class(VIEW3D_PT_ta_tools)

if __name__ == "__main__":
    register()
