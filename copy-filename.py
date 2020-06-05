#!/usr/bin/env python3
"""
Author: ttyS3
copy selected filename
"""

import datetime
import os
import subprocess

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

def main():
    filenames = []
    for path in os.getenv('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS','').splitlines():
        try:
            filenames.append(os.path.basename(path))
        except OSError:
            continue
    clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clip.set_text("\n".join(filenames), -1)

    # MessageDialog just for debug
    md = Gtk.MessageDialog(parent=None, 
    flags=0, message_type=Gtk.MessageType.INFO, 
    buttons=Gtk.ButtonsType.CLOSE, text="\n".join(filenames))
    md.run()
    md.destroy()

if __name__ == '__main__':
    main()