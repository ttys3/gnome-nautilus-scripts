# gnome-nautilus-scripts

GNOME nautilus file manager scripts

## usage

put it under `~/.local/share/nautilus/scripts` and have fun -_-

## included scripts

1. `copy-filename.py`: copy base filename to clipboard

2. `copy-filepath.py`: copy full path filename to clipboard

## dev

### method 1: use exists stubs

```bash
pip install --user PyGObject-stubs
```

### method 2: make the stubs yourself

see <https://github.com/pygobject/pygobject-stubs/issues/5#issuecomment-639541725>

> if you do NOT have pycharm installed, you need to clone the intellij-community repo:
> `git clone --depth 1 https://github.com/JetBrains/intellij-community.git /tmp/idea`
>
> and replace the command below
>
> `PYTHONPATH=$HOME/Apps/pycharm-community/plugins/python-ce/helpers python3 -m generator3`
>
> with
> 
> `python3 /tmp/idea/python/helpers/generator3/__main__.py`


```bash
mkdir /tmp/out
for typelib in Atk GLib GModule GObject Gdk GdkPixbuf Gio Gtk Pango; do
    PYTHONPATH=$HOME/Apps/pycharm-community/plugins/python-ce/helpers python3 -m generator3 -d /tmp/out -p gi.repository.$typelib $(python3 -c "import gi; gi.require_versions({'Atk': '1.0', 'GModule': '2.0', 'Gdk': '3.0', 'GdkPixbuf': '2.0', 'Gtk': '3.0', 'Pango': '1.0'}); from gi.repository import $typelib; print($typelib.__path__[-1])")
done

#make pyCharm can use it:
mv /tmp/out/gi ~/.local/lib/python3.8/site-packages/gi-stubs
# or you can put the gi-stubs dir to anywhere but just remember to add to your project
# see https://www.jetbrains.com/help/pycharm/stubs.html#reuse-stubs
```

`$HOME/Apps/pycharm-community` is the pycharm installation path of mine, please use your own path.

explain:

`python3 -c "import gi; gi.require_versions({'Gtk': '3.0'}); from gi.repository import Gtk; print(Gtk.__path__[-1])"` will ouput

`/usr/lib64/girepository-1.0/Gtk-3.0.typelib`

when we run 

`PYTHONPATH=$HOME/Apps/pycharm-community/plugins/python-ce/helpers python3 -m generator3 -d /tmp/out -p gi.repository.Gtk /usr/lib64/girepository-1.0/Gtk-3.0.typelib`

the JetBrains generator3 will generate stubs for `gi.repository.Gtk` package by parsing the G-IR binary database file `/usr/lib64/girepository-1.0/Gtk-3.0.typelib`