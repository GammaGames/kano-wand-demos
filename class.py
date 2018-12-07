from kano_wand.kano_wand import Shop, Wand, PATTERN
import sys

# Custom wand class extending the default wand
class MyWand(Wand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colors = ["#a333c8", "2185d0", "0x21ba45", "#fbbd08", "#f2711c", "#db2828"]

    # Do some functions after connecting
    def post_connect(self):
        print("Connected to {}".format(self.name))
        # Vibrate the wand and set its color to red
        self.vibrate(PATTERN.BURST)
        self.set_led(self.colors.pop())
        # Subscribe to notifications
        self.subscribe_button()
        self.subscribe_position()

    # Button callback, automatically called after connecting to wand
    def on_button(self, pressed):
        if pressed:
            self.unsubscribe_position()
            # Update the led
            self.set_led(self.colors.pop())
            # Disconnect if we run out of colors
            if len(self.colors) == 0:
                self.disconnect()

    # Position callback, automatically called after connecting to wand
    def on_position(self, x, y, pitch, roll):
        pitch = "Pitch: {}".format(pitch).ljust(16)
        roll = "Roll: {}".format(roll).ljust(16)
        print("{}{}(x, y): ({}, {})".format(pitch, roll, x, y))

def main():
    # If we pass a -d flag, enable debugging
    debug = False
    if len(sys.argv) > 1:
        debug = sys.argv[1] == "-d"

    # Create a new wand scanner
    shop = Shop(wand_class=MyWand, debug=debug)
    wands = []
    try:
        # While we don't have any wands
        while len(wands) == 0:
            # Scan for wands and automatically connect
            print("Scanning...")
            wands = shop.scan(connect=True)

    # Detect keyboard interrupt and disconnect wands
    except KeyboardInterrupt as e:
        for wand in wands:
            wand.disconnect()

if __name__ == "__main__":
    main()
