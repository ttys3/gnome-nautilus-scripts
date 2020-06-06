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
import traceback

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Notify

log_file = "/tmp/ImageMagick-strip.txt"

# use the `>` flag, resize only when the image is bigger
resize_to = "1920x1080>"

app_name = os.path.basename(__file__)

def main():
    try:
        os.remove(log_file)
    except FileNotFoundError:
        pass

    try:
        total = 0
        for path in os.getenv('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS', '').splitlines():
            total += strip_exif(path)
        send_notification(app_name, "successfully processed file: {}".format(total))
    except Exception:
        show_err(traceback.format_exc())


def is_image(path):
    if not os.path.isfile(path):
        return False
    allowed_filetypes = ('.png', '.jpg', '.jpeg', '.webp', '.tiff', '.bmp', '.gif')
    if not path.lower().endswith(allowed_filetypes):
        return False
    ft = imghdr.what(path)
    if ft is None:
        return False
    if not ('.' + ft) in allowed_filetypes:
        return False
    return True


def exec_strip_cmd(path):
    if not is_image(path):
        return 0

    f = open(log_file, "a")
    f.write(path + "\n")
    try:
        # convert [input-option] input-file [output-option] output-file
        outpath = path
        # when using -resize, resize a png to smaller resolution usually makes the size get bigger
        # re-encode it to jpeg file will keep the size almost the same or slightly smaller
        # see http://www.imagemagick.org/discourse-server/viewtopic.php?t=35439
        # http://www.imagemagick.org/Usage/resize/
        if "png" == imghdr.what(path):
            outpath = path.rstrip(".png").rstrip(".PNG") + ".jpg"
        strip_meta = subprocess.run(["convert", path, "-strip", "-resize", resize_to, outpath], stdout=f)
        strip_meta.check_returncode()
        return 1
    except subprocess.CalledProcessError as err:
        show_err(err)
        raise err
    finally:
        if f: f.close()


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
            total += exec_strip_cmd(entry.path)
    return total


def show_info(msg):
    md = Gtk.MessageDialog(parent=None,
                           flags=0,
                           message_type=Gtk.MessageType.INFO,
                           buttons=Gtk.ButtonsType.CLOSE,
                           text=msg
                           )
    md.run()
    md.destroy()
    sys.exit()


def show_err(msg):
    md = Gtk.MessageDialog(parent=None,
                           flags=0,
                           message_type=Gtk.MessageType.ERROR,
                           buttons=Gtk.ButtonsType.CLOSE,
                           text=msg
                           )
    md.run()
    md.destroy()
    sys.exit()


def send_notification(title, text, file_path_to_icon=""):
    n = Notify.Notification.new(title, text, file_path_to_icon)
    n.show()

if __name__ == '__main__':
    # One time initialization of libnotify
    Notify.init(app_name)
    main()
