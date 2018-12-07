from kano_wand.kano_wand import Shop, Wand, PATTERN
import moosegesture
import sys

class GestureWand(Wand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pressed = False
        self.positions = []

    def post_connect(self):
        print("Hold the button, move the wand, and release the button to create gestures")
        print("Draw a counterclockwise circle (starting at the bottom) to disconnect the wand")
        self.subscribe_button()
        self.subscribe_position()

    def on_position(self, x, y, pitch, roll):
        if self.pressed:
            # Add the mouse's position to the positions array
            self.positions.append(tuple([x, -1 * y]))

    def on_button(self, pressed):
        self.pressed = pressed

        if not pressed:
            # If releasing the button, print out the gestures and reset the positions
            gesture = moosegesture.getGesture(self.positions)
            self.positions = []

            print(gesture)
            # If it is a counterclockwise circle disconnect the wand
            if gesture == ['R', 'UR', 'U', 'UL', 'L', 'DL', 'D', 'DR', 'R']:
                self.disconnect()

def main():
    # If we pass a -d flag, enable debugging
    debug = False
    if len(sys.argv) > 1:
        debug = sys.argv[1] == "-d"

    # Create a new wand scanner
    shop = Shop(wand_class=GestureWand, debug=debug)
    wands = []
    try:
        # While we don't have any wands
        while len(wands) == 0:
            print("Scanning...")
            # Scan for wands and automatically connect
            wands = shop.scan(connect=True)

    # Detect keyboard interrupt and disconnect wands
    except KeyboardInterrupt as e:
        for wand in wands:
            wand.disconnect()

if __name__ == "__main__":
    main()
