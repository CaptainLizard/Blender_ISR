# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Incrementaly Save Render",
    "author": "Captain_lizard",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "Image editor -> Panel -> Save",
    "description": "Incrementaly saves the image",
    "warning": "Don't forget to define the ouput of the rendered images first",
    "category": "Render"}


import bpy
from bpy.types import Panel, Operator
from os.path import dirname, join, exists
from os import mkdir, listdir
from re import findall

class RENDER_OT_incremental_save(Operator):
    """Incrementally save the rendered image"""
    bl_idname = "render.incremental_save"
    bl_label = "Incremental Save"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        render = scene.render

        # Check if Render Result exists
        image = bpy.data.images.get('Render Result')
        if image is None:
            self.report({'ERROR'}, "Render Result not found")
            return {'CANCELLED'}

        # Determine the filepath for saving
        output_path = bpy.path.abspath(render.filepath)
        if not output_path:
            self.report({'ERROR'}, "Output filepath not set")
            return {'CANCELLED'}

        blendname = bpy.path.basename(output_path).rpartition('.')[0]
        filepath = join(dirname(output_path), 'auto_saves')
        if not exists(filepath):
            mkdir(filepath)

        # Get a list of existing files with the blendname
        files = [f for f in listdir(filepath)
                 if f.startswith(blendname)]

        # Find the next available number for incremental save
        save_number = 1
        if files:
            save_number = max([int(findall(r'\d+', f)[-1]) for f in files]) + 1

        # Save the image
        save_name = f"{blendname}_{bpy.path.basename(output_path)}_{str(save_number).zfill(3)}.{render.image_settings.file_format.lower()}"
        save_path = join(filepath, save_name)
        image.save_render(save_path, scene=None)

        self.report({'INFO'}, f"Saved: {save_path}")
        return {'FINISHED'}


class RENDER_PT_incremental_save_panel(Panel):
    bl_label = "Incremental Save"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Save'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.operator("render.incremental_save", text="Save Incrementally")


def register():
    bpy.utils.register_class(RENDER_OT_incremental_save)
    bpy.utils.register_class(RENDER_PT_incremental_save_panel)


def unregister():
    bpy.utils.unregister_class(RENDER_OT_incremental_save)
    bpy.utils.unregister_class(RENDER_PT_incremental_save_panel)


if __name__ == "__main__":
    register()
