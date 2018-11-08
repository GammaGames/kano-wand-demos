# Kano Wand Demos
Demos using the [Kano Wand python module](https://github.com/GammaGames/kano_wand)

## Usage
For these demos I added the kano_wand repo as a submodule.
In order to use these demos you must clone the submodule using one of the following:

```sh
# If you are just cloning the repo
git clone --recursive git@github.com:GammaGames/kano-wand-demos.git
# If you have already cloned it and need to update the submodules
git submodule init
git pull --recurse-submodules
```

All demos must be run with sudo, because bluepy's ble requires elevation to scan.

You can pass a `-d` flag into each script to enable printing of debug messages.

## demo_callback.py

## demo_class.py

## demo_mixed.py

## demo_mouse.py
