# Kano Wand Demos

Demos using the [Kano Wand python module](https://github.com/GammaGames/kano_wand)

## Cloning this repo

For these demos I added the kano_wand repo as a submodule.
In order to use these demos you must clone the submodule using one of the following:
```sh
# If you are cloning the repo from nothing
git clone --recursive git@github.com:GammaGames/kano-wand-demos.git
# If you have already cloned this repo and need to update the submodules
git submodule init
git pull --recurse-submodules
```

Then install the requirements with the following:
```sh
pip install -r requirements.txt
```

## Usage

All demos must be run with sudo, because bluepy's ble requires elevation to scan. You can pass a `-d` flag into each script to enable printing of debug messages. For example, to run the callback demo with debugging enabled you should use the following:
```sh
sudo python3 callback.py -d
```
All demos are commented and should be nice 

### callback<span></span>.py

This demo scans for the wand, and after connecting does the following:
1. Makes the wand vibrate
2. Sets the wand's led to red
3. Adds a callback for the position event
    * When the wand receives a new position, it prints the position data to the console.
4. Adds a callback for the button event
    * On the first button press, it removes the callback for the position event
    * On each button press the led changes color down the rainbow. On purple (6 presses), the wand disconnects

### class<span></span>.py

This demo is the same as the callback.py demo, but it uses a custom class instead of callbacks. It does this by passing `wand_class=MyWand` into the Shop's constructor.  
The MyWand class inherits from the kano_wand.Wand class, and uses the following functions:
1.  `post_connect`
    * Vibrate and set wand led
    * Subscribe to button and position events
2. `on_button`
    * Unsubscribe from the position callback on the first button press
    * Change the led and disconnect after 6 presses
3. `on_position`
    * Print the position data to the console

### mixed<span></span>.py

This demo does the same as the callback.py demo, but it subscribes to the button event in the MyWand class and subscribes to the position event with a callback. The button press removes the callback via its id.

### mouse<span></span>.py

This demo is a little more fun, it lets you move the mouse around on your screen with the wand! You can tilt the wand left to left click and right to right click. By tilting the wand left, holding the button down, tilting the wand right, and letting to fo the button you can disconnect the wand and exit the demo.

### gesture<span></span>.py

This is a more proof-of-concept demo. It uses moosegesture to print out movements (arrays of directions, for example `['U', 'D', 'UR']`). It prints out direction arrays, and you can draw a counterclockwise circle to disconnect the wand. Further work can be done to use the wand gestures from the Kano app, as well.

### hue<span></span>.py

This is a demo to control your phillips hue light bulbs with the wand. Perform gestures (based on the included Kano wand motions poster) to make the bulb do different effects! [Here's a full writeup in a Medium article.](https://medium.com/@jesse007.gg/control-a-phillips-hue-bulb-with-the-flick-of-a-wand-3a9af4826775)
