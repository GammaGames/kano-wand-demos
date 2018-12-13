from kano_wand.kano_wand import Shop, Wand, PATTERN
from qhue import Bridge
import moosegesture as mg
import time
import random
import math

class GestureWand(Wand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Basic gesture dictionary
        # We use them as tuples so we can use them as keys
        self.gestures = {
            ("DL", "R", "DL"): "stupefy",
            ("DR", "R", "UR", "D"): "wingardium_leviosa",
            ("UL", "UR"): "reducio",
            ("DR", "U", "UR", "DR", "UR"): "flipendo",
            ("R", "D"): "expelliarmus",
            ("UR", "U", "D", "UL", "L", "DL"): "incendio",
            ("UR", "U", "DR"): "lumos",
            ("U", "D", "DR", "R", "L"): "locomotor",
            ("DR", "DL"): "engorgio",
            ("UR", "R", "DR"): "aguamenti",
            ("UR", "R", "DR", "UR", "R", "DR"): "avis",
            ("D", "R", "U"): "reducto"
        }
        self.spell = None
        self.pressed = False
        self.positions = []

    def post_connect(self):
        self.subscribe_button()
        self.subscribe_position()

    def on_position(self, x, y, pitch, roll):
        if self.pressed:
            # While holding the button,
            #   append the position to the positions array
            self.positions.append(tuple([x, -1 * y]))

    def on_button(self, pressed):
        self.pressed = pressed

        if pressed:
            self.spell = None
        else:
            # If releasing the button, get the gesture
            gesture = mg.getGesture(self.positions)
            self.positions = []
            closest = mg.findClosestMatchingGesture(gesture, self.gestures, maxDifference=1)

            if closest != None:
                # Just use the first gesture in the list using the gesture key
                self.spell = self.gestures[closest[0]]
                self.vibrate(PATTERN.SHORT)
            # Print out the gesture
            print("{}: {}".format(gesture, self.spell))

class LightManager():
    def __init__(self):
        # Dictionary of bulb color effects
        self.color_values = {
            None: {"on": True, "bri": 144, "hue": 7676, "sat": 199},
            "stupefy": {"hue": 0, "bri": 200, "sat": 150},
            "wingardium_leviosa": {"hue": 37810, "bri": 100, "sat": 40},
            "reducio": {"hue": 51900, "bri": 200, "sat": 200},
            "flipendo": {"hue": 37445, "bri": 150, "sat": 140},
            "expelliarmus": {"hue": 1547, "bri": 200, "sat": 200},
            "incendio": {"hue": 7063, "bri": 200, "sat": 250},
            "lumos": {"hue": 0, "bri": 204, "sat": 0},
            "locomotor": {"hue": 12324, "bri": 100, "sat": 140},
            "engorgio": {"hue": 32275, "bri": 125, "sat": 120},
            "aguamenti": {"hue": 32275, "bri": 180, "sat": 200},
            "avis": {"hue": 37445, "bri": 150, "sat": 130},
            "reducto": {"hue": 37445, "bri": 180, "sat": 200}
        }
        self.current = self.color_values[None]
        # Bridge api values
        self.bridge_ip = "192.168.1.22"
        self.username = "dBHN8d6Qkw6EJMqzEI2oI0zXJGiOdvyE2lRzFha8"
        # Bridge object and lights
        self.bridge = Bridge(self.bridge_ip, self.username)
        self.light_ids = ["1"]
        self.light_states = {}

        for id in self.light_ids:
            # Backup the state of all the lights
            light = self.bridge.lights[id]
            state = {"on": True, **self.color_values[None]}
            s = light()['state']
            for key in state:
                state[key] = s.get(key)
            self.light_states[id] = state
            # Set the default state for the bulb
            light.state(on=True, **self.color_values[None])

    # Flicker the bulbs with wand effects
    def flicker(self, spell, transition):

        for id in self.light_ids:
            light = self.bridge.lights[id]
            on = light()['state']['on']
            self.current = self.color_values[spell]

            if spell == "lumos":
                # Toggle the bulb on lumos
                light.state(transitiontime=transition, on=not on, **self.current)
            elif on:
                # Else set the bulb to a small brightness offset
                c = self.current.copy()
                c["bri"] = c["bri"] + random.randint(0, 53)
                light.state(transitiontime=transition, **c)

    # Reset all bulbs to their initial state
    def reset(self):
        for id in self.light_ids:
            light = self.bridge.lights[id]
            light.state(**self.light_states[id])

def main():
    # Create the manager and shop to search for wands
    manager = LightManager()
    shop = Shop(wand_class=GestureWand)
    wands = []

    try:
        # Scan for wands until it finds some
        while len(wands) == 0:
            print("Scanning...")
            wands = shop.scan(connect=True)

        wand = wands[0]
        while wand.connected:
            # Make a random sleep and transition time
            sleep = random.uniform(0.1, 0.2)
            transition = math.ceil(sleep * 10)
            # Flicker the bulb and sleep
            manager.flicker(wand.spell, transition)
            if wand.spell == "lumos":
                wand.spell = None
            time.sleep(sleep)

        # Reset bulbs to initial state when wand disconnects
        manager.reset()

    # Detect keyboard interrupt and disconnect wands, reset light
    except KeyboardInterrupt as e:
        for wand in wands:
            wand.disconnect()
        manager.reset()

if __name__ == "__main__":
    main()
