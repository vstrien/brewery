import curses
import re
import time
# Load settings
import configparser
config = configparser.ConfigParser()
config.read('settings.ini')

heatelement = config['devices']['heatelement']
tube = config['devices']['tube']

def read_sensor(path):
    value = "U"
    with open(path, "r") as f:
        line = f.readline()
        if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
            line = f.readline()
            m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
            if m:
                value = float(m.group(2)) / 1000.0
    return value

# Get current date-time stamp in yyyymmddhhmmss format

logfile = f"log_{time.strftime('%Y%m%d%H%M%S')}.txt"

def main(stdscr):
    stdscr.nodelay(True)

    # Clear screen
    stdscr.clear()
    
    while True:
        # Display the current temperature at the top of the screen

        stdscr.clear()
        heat_element_temp = read_sensor(heatelement)
        tube_temp = read_sensor(tube)

        stdscr.addstr(0, 0, "Temperatures")
        stdscr.addstr(1, 0, "|")
        stdscr.addstr(2, 0, "+-- Element: {} C".format(heat_element_temp))
        stdscr.addstr(3, 0, "|")
        stdscr.addstr(4, 0, "+-- Tube   : {} C".format(tube_temp))

        with open(logfile, "a") as f:
            f.write("{}\tE:{}\tT:{}\n".format(time.strftime('%Y%m%d%H%M%S'), heat_element_temp, tube_temp))

        ch = stdscr.getch()
        if ch == ord('q'):
            break

        time.sleep(0.5)
        
        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)