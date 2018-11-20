import moosegesture
from kano_wand.kano_wand import Shop, Wand, PATTERN

if __name__ == "__main__":
    class GestureWand(Wand):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.pressed = False
            self.positions = []

        def post_connect(self):
            print("Hold the button, move the wand, and release the button to create gestures")
            print("Draw a counterclockwise circle to disconnect the wand")
            self.subscribe_button()
            self.subscribe_position()

        def on_position(self, x, y, pitch, roll):
            if self.pressed:
                self.positions.append(tuple([-x, -y]))

        def on_button(self, pressed):
            self.pressed = pressed

            if not pressed:
                gesture = moosegesture.getGesture(self.positions)
                self.positions = []

                print(gesture)
                if gesture == ['R', 'UR', 'U', 'UL', 'L', 'DL', 'D', 'DR']:
                    self.disconnect()

    # Create a new wand scanner
    shop = Shop(wand_class=GestureWand)
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
