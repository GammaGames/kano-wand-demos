from kano_wand.kano_wand import Shop, PATTERN
import time
import sys

def main():
    # If we pass a -d flag, enable debugging
    debug = False
    if len(sys.argv) > 1:
        debug = sys.argv[1] == "-d"

    # Create a new wand scanner
    shop = Shop(debug=debug)
    wands = []
    try:
        # While we don't have any wands
        while len(wands) == 0:
            # Scan for wands and automatically connect
            print("Scanning...")
            wands = shop.scan(connect=True)
            # For each wand (Only tested with one)
            for wand in wands:
                print("Connected to {}".format(wand.name))

                colors = ["#a333c8", "2185d0", "0x21ba45", "#fbbd08", "#f2711c", "#db2828"]
                # Vibrate the wand and set its color to red
                wand.vibrate(PATTERN.BURST)
                wand.set_led(colors.pop())

                # Callback for position
                def onPos(x, y, pitch, roll):
                    pitch = "Pitch: {}".format(pitch).ljust(16)
                    roll = "Roll: {}".format(roll).ljust(16)
                    print("{}{}(x, y): ({}, {})".format(pitch, roll, x, y))

                # Add the position callback to the wand
                position_id = wand.on("position", onPos)

                # Callback for button presses
                def onButton(pressed):
                    global wand
                    global colors
                    global position_id

                    # If the button was pressed
                    if pressed:
                        if position_id != None:
                            wand.off(position_id)
                            position_id = None
                        # Update the led
                        wand.set_led(colors.pop())
                        # Disconnect if we run out of colors
                        if len(colors) == 0:
                            wand.disconnect()

                # Add the button callback to the wand
                wand.on("button", onButton)

    # Detect keyboard interrupt and disconnect wands
    except KeyboardInterrupt as e:
        for wand in wands:
            wand.disconnect()

if __name__ == "__main__":
    main()
