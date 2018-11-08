from kano_wand.kano_wand import Shoppe, Wand, PATTERN
import sys

if __name__ == "__main__":
    # Custom wand class extending the default wand
    class MyWand(Wand):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.colors = ["#a333c8", "2185d0", "0x21ba45", "#fbbd08", "#f2711c", "#db2828"]

        # Do some functions after connecting
        def post_connect(self):
            print(f"Connected to {self.name}")
            # Vibrate the wand and set its color to red
            self.set_led(self.colors.pop())
            # Subscribe to notifications
            self.subscribe_button()

        # Button callback, automatically called after connecting to wand
        def on_button(self, value):
            # If the button was pressed
            if value:
                # Update the led
                self.set_led(self.colors.pop())
                # Disconnect if we run out of colors
                if len(self.colors) == 0:
                    self.disconnect()

    # If we pass a -d flag, enable debugging
    debug = False
    if len(sys.argv) > 1:
        debug = sys.argv[1] == "-d"

    # Create a new wand scanner
    shoppe = Shoppe(wand_class=MyWand, debug=debug)
    wands = []
    try:
        # While we don't have any wands
        while len(wands) == 0:
            # Scan for wands and automatically connect
            print("Scanning...")
            wands = shoppe.scan(connect=True)
            # For each wand (Only tested with one)
            for wand in wands:
                # Vibrate the wand and set its color to red
                wand.vibrate(PATTERN.BURST)

                # Callback for position
                def onPos(x, y, pitch, roll):
                    pitch = f"Pitch: {pitch}".ljust(16)
                    roll = f"Roll: {roll}".ljust(16)
                    print(f"{pitch}{roll}(x, y): ({x}, {y})")

                # Add the event callback to the wand
                wand.on("position", onPos)

    # Detect keyboard interrupt disconnect
    except KeyboardInterrupt as e:
        for wand in wands:
            wand.disconnect()