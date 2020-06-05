#!/usr/bin/env python3
"""
Author: ttyS3
copy selected filename path
"""

import os
import gi

gi.require_versions({'Gdk': '3.0', 'Gtk': '3.0'})
from gi.repository import Gtk, Gdk, GLib


def main():
    dirpath = ""
    paths = os.getenv('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS', '').splitlines()
    if len(paths) > 0:
        dirpath = os.path.dirname(paths[0])

    clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clip.set_text(dirpath, -1)
    clip.store()
    GLib.timeout_add(100, Gtk.main_quit)
    Gtk.main()

    # MessageDialog just for debug
    if os.path.exists("/tmp/nautilus.scripts.debug"):
        md = Gtk.MessageDialog(parent=None,
                               flags=0,
                               message_type=Gtk.MessageType.INFO,
                               buttons=Gtk.ButtonsType.CLOSE,
                               text=dirpath
                               )
        md.run()
        md.destroy()


if __name__ == '__main__':
    main()
