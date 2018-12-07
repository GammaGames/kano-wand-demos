from kano_wand.kano_wand import Shop, Wand
import sys
from pymouse import PyMouse

if __name__ == "__main__":
    class MouseWand(Wand):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.left_color = "#2185d0"
            self.right_color = "#f2711c"
            self.left = False
            self.pressed_left = False

        def post_connect(self):
            print("Move the wand to move the mouse")
            print("Tilt the want to the left (blue light) to left click")
            print("Tilt the want to the right (orange light) to right click")
            print("Tilt the wand left, hold the button, tilt the wand to the right, and release the button to disconnect")
            # Create a mouse and get the screen dimensions
            self._m = PyMouse()
            self.x_dim, self.y_dim = self._m.screen_size()
            self.set_led(self.left_color)

            self.subscribe_button()
            self.subscribe_position()

        def on_position(self, x, y, pitch, roll):
            # Do some magic to get an adjusted x and y position
            x_pos = self.x_dim * ((x * 4 + 1000) / 2000)
            y_pos = self.y_dim * (1.0 - (y * 4 + 1000) / 2000)
            # Move the mouse
            self._m.move(int(round(x_pos)), int(round(y_pos)))

            # Change left mouse button status and set LED when necessary
            if roll > 0 and self.left:
                self.left = False
                self.set_led(self.right_color)
            elif roll < 0 and not self.left:
                self.left = True
                self.set_led(self.left_color)

        def on_button(self, pressed):
            x_pos, y_pos = self._m.position()
            if pressed:
                self._m.press(x_pos, y_pos, 1 if self.left else 2)
                self.pressed_left = self.left
            else:
                self._m.release(x_pos, y_pos, 1 if self.left else 2)
                if self.pressed_left and not self.left:
                    self.disconnect()

    # If we pass a -d flag, enable debugging
    debug = False
    if len(sys.argv) > 1:
        debug = sys.argv[1] == "-d"

    # Create a new wand scanner
    shop = Shop(wand_class=MouseWand, debug=debug)
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
