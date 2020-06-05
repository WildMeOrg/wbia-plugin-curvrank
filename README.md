# WBIA CurvRank Plugin
An wbia plugin wrapper for https://github.com/hjweide/dolphin-identification#functional

# Requirements

* OpenCV (cv2)

# Installation

Install this plugin as a Python module using

```bash
cd ~/code/wbia-plugin-curvrank/
pip install -e .
```

With the plugin installed, register the module name with the `IBEISControl.py` file
in the wildbook-ia repository located at `wildbook-ia/wbia/control/IBEISControl.py`.  Register
the module by adding the string (for example, `wbia_curvrank`) to the
list `AUTOLOAD_PLUGIN_MODNAMES`.

# Example
```
$ python
>>> import wbia_curvrank
>>> wbia_curvrank._plugin.wbia_plugin_curvrank_example(None)
```
