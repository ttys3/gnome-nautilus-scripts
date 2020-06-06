#!/usr/bin/env python3
"""
Author: ttyS3
strip all meta info of image using ImageMagick convert
!!! WARNING:
    ImageMagick convert will do strip with recompression every time,
    so the file content will change every time

show all exif meta:
identify -verbose IMG_9522.JPG | grep -i exif
exiftool -a -u -g1 IMG_9522.JPG
exiv2 -pa pr IMG_9522.JPG
"""

import datetime
import os
import subprocess
import sys
import imghdr

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

log_file = "/tmp/ImageMagick-strip.txt"


def main():
    try:
        os.remove(log_file)
    except NotImplementedError:
        pass

    for path in os.getenv('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS', '').splitlines():
        strip_exif(path)


def is_image(path):
    if not os.path.isfile(path):
        return False
    allowed_filetypes = ('.png', '.jpg', '.jpeg', '.webp', '.tiff', '.bmp', '.gif')
    if not path.lower().endswith(allowed_filetypes):
        return False
    if not ('.' + imghdr.what(path)) in allowed_filetypes:
        return False
    return True


def exec_strip_cmd(path):
    if not is_image(path):
        return

    f = open(log_file, "a")
    f.write(path + "\n")
    try:
        # convert [input-option] input-file [output-option] output-file
        # resize only image is bigger
        strip_meta = subprocess.run(["convert", path, "-resize", "1920x1080>", "-strip", path], stdout=f)
        strip_meta.check_returncode()
        f.close()
    except subprocess.CalledProcessError as err:
        show_err(err)
        f.close()
        raise err


def strip_exif(path):
    if os.path.isfile(path):
        exec_strip_cmd(path)
        return 1
    total = 0
    for entry in os.scandir(path):
        try:
            is_dir = entry.is_dir(follow_symlinks=False)
        except OSError as error:
            print('Error calling is_dir():', error, file=sys.stderr)
            continue
        if is_dir:
            total += strip_exif(entry.path)
        else:
            exec_strip_cmd(entry.path)
            total += 1
    return total


def show_err(msg):
    md = Gtk.MessageDialog(parent=None,
                           flags=0,
                           message_type=Gtk.MessageType.INFO,
                           buttons=Gtk.ButtonsType.CLOSE,
                           text=msg
                           )
    md.run()
    md.destroy()
    sys.exit()


if __name__ == '__main__':
    main()
