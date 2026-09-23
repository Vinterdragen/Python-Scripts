#!/usr/bin/env python3
"""
GIMP 3.x plug-in: Texture Packer
Combines N selected image files into a single grid-atlas image.

Layout: auto square-ish grid (cols = ceil(sqrt(n)), rows = ceil(n/cols)).
Tile size: taken from whichever single input image has the largest pixel
area (so the tile always matches one real input's dimensions, rather than
mixing the widest image's width with a different image's height).
Each input is scaled to fill its tile exactly (aspect ratio is NOT
preserved -- this assumes same-size-ish source textures, which matches
the "8x 1024 -> atlas" use case it was built for).

Install:
  Copy this whole folder to:
    %APPDATA%\GIMP\3.2\plug-ins\texture-packer\texture-packer.py
  Restart GIMP, then use (no image needs to be open):
    Filters > Texture Packer > Pack Textures into Atlas...
"""

import sys
import math

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
from gi.repository import GLib
from gi.repository import Gio
from gi.repository import Gtk


def _(s):
    return s


PROC_NAME = "plug-in-texture-packer"


class TexturePacker(Gimp.PlugIn):

    def do_query_procedures(self):
        return [PROC_NAME]

    def do_set_i18n(self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN, self.run, None
        )
        procedure.set_image_types("*")
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)
        procedure.set_menu_label(_("Pack Textures into Atlas..."))
        procedure.add_menu_path("<Image>/Filters/Texture Packer")
        procedure.set_documentation(
            _("Pack multiple textures into one grid atlas"),
            _("Select several image files; they are arranged into an "
              "auto square-ish grid and combined into a single image."),
            name,
        )
        procedure.set_attribution("Simon Carmona @Vinterdragen", "Simon Carmona @Vinterdragen", "2026")
        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if run_mode != Gimp.RunMode.INTERACTIVE:
            return procedure.new_return_values(
                Gimp.PDBStatusType.CALLING_ERROR, GLib.Error()
            )

        GimpUi.init("texture-packer")

        input_files = self._choose_input_files()
        if not input_files:
            return procedure.new_return_values(
                Gimp.PDBStatusType.CANCEL, GLib.Error()
            )

        output_file = self._choose_output_file()
        if not output_file:
            return procedure.new_return_values(
                Gimp.PDBStatusType.CANCEL, GLib.Error()
            )

        try:
            atlas_image = self._pack(input_files)
        except Exception as e:
            Gimp.message(f"Texture Packer failed: {e}")
            return procedure.new_return_values(
                Gimp.PDBStatusType.EXECUTION_ERROR, GLib.Error()
            )

        try:
            Gimp.file_save(
                Gimp.RunMode.NONINTERACTIVE, atlas_image, output_file, None
            )
        except Exception as e:
            atlas_image.delete()
            Gimp.message(f"Texture Packer failed to save: {e}")
            return procedure.new_return_values(
                Gimp.PDBStatusType.EXECUTION_ERROR, GLib.Error()
            )

        Gimp.Display.new(atlas_image)
        Gimp.displays_flush()

        return procedure.new_return_values(
            Gimp.PDBStatusType.SUCCESS, GLib.Error()
        )

    def _choose_input_files(self):
        dialog = Gtk.FileChooserDialog(
            title=_("Select textures to pack"),
            action=Gtk.FileChooserAction.OPEN,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
        )
        dialog.set_select_multiple(True)

        img_filter = Gtk.FileFilter()
        img_filter.set_name(_("Images"))
        for pattern in ("*.png", "*.jpg", "*.jpeg", "*.tga", "*.bmp", "*.tiff", "*.exr"):
            img_filter.add_pattern(pattern)
        dialog.add_filter(img_filter)

        files = []
        if dialog.run() == Gtk.ResponseType.OK:
            files = dialog.get_filenames()
        dialog.destroy()
        return files

    def _choose_output_file(self):
        dialog = Gtk.FileChooserDialog(
            title=_("Save atlas as"),
            action=Gtk.FileChooserAction.SAVE,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE, Gtk.ResponseType.OK,
        )
        dialog.set_current_name("atlas.png")
        dialog.set_do_overwrite_confirmation(True)

        out_path = None
        if dialog.run() == Gtk.ResponseType.OK:
            out_path = dialog.get_filename()
        dialog.destroy()

        if not out_path:
            return None
        return Gio.File.new_for_path(out_path)

    def _pack(self, input_paths):
        loaded = []
        atlas = None
        try:
            max_w = 0
            max_h = 0
            best_area = -1
            for path in input_paths:
                gfile = Gio.File.new_for_path(path)
                img = Gimp.file_load(Gimp.RunMode.NONINTERACTIVE, gfile)
                loaded.append(img)
                w, h = img.get_width(), img.get_height()
                if w * h > best_area:
                    best_area = w * h
                    max_w, max_h = w, h

            n = len(loaded)
            cols = math.ceil(math.sqrt(n))
            rows = math.ceil(n / cols)

            atlas_w = cols * max_w
            atlas_h = rows * max_h

            atlas = Gimp.Image.new(atlas_w, atlas_h, Gimp.ImageBaseType.RGB)

            for i in range(n):
                src_img = loaded[i]
                src_img.flatten()
                drawables = src_img.get_selected_drawables()
                if not drawables:
                    raise RuntimeError(f"no drawable found in {input_paths[i]}")
                drawable = drawables[0]

                layer = Gimp.Layer.new_from_drawable(drawable, atlas)
                atlas.insert_layer(layer, None, -1)

                if layer.get_width() != max_w or layer.get_height() != max_h:
                    layer.scale(max_w, max_h, False)

                col = i % cols
                row = i // cols
                layer.set_offsets(col * max_w, row * max_h)

                src_img.delete()
                loaded[i] = None

            atlas.flatten()
            return atlas
        except Exception:
            for img in loaded:
                if img is not None:
                    img.delete()
            if atlas is not None:
                atlas.delete()
            raise


Gimp.main(TexturePacker.__gtype__, sys.argv)
