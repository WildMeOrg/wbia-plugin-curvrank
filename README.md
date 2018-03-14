# IBEIS CurveRank Plugin
An ibeis plugin wrapper for https://github.com/hjweide/dolphin-identification#functional

# Requirements

* OpenCV (cv2)

# Installation

Install this plugin as a Python module using

```bash
cd ~/code/ibeis-curverank-module/
pip install -e .
```

With the plugin installed, register the module name with the `IBEISControl.py` file
in the ibeis repository located at `ibeis/ibeis/control/IBEISControl.py`.  Register
the module by adding the string (for example, `ibeis_curverank`) to the
list `AUTOLOAD_PLUGIN_MODNAMES`.

# Example
```
$ python
>>> import ibeis_curverank
>>> ibeis_curverank._plugin.ibeis_plugin_curverank_example(None)
```