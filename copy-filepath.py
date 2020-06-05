#!/usr/bin/env python3
"""
Author: ttyS3
copy selected file path
"""

import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib


def main():
    clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    filenames = os.getenv('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS', '').strip()
    clip.set_text(filenames, -1)
    GLib.timeout_add(100, Gtk.main_quit)
    Gtk.main()

    # MessageDialog just for debug
    if os.path.exists("/tmp/nautilus.scripts.debug"):
        md = Gtk.MessageDialog(parent=None,
                               flags=0,
                               message_type=Gtk.MessageType.INFO,
                               buttons=Gtk.ButtonsType.CLOSE,
                               text=filenames)
        md.run()
        md.destroy()


if __name__ == '__main__':
    main()
