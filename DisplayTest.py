import curses
import random
import time

def main(stdscr):
    stdscr.nodelay(True)

    # Clear screen
    stdscr.clear()
    input_str = ""
    
    while True:
        # Display the current temperature at the top of the screen

        stdscr.clear()
        newtemp = random.randint(0, 100)
        stdscr.addstr(0, 0, "Current temperature: {} C".format(newtemp))

        # Get user input at the bottom of the screen
        stdscr.addstr(curses.LINES - 1, 0, f"Enter the desired temperature (C) or STOP to stop the program: {input_str}")

        ch = stdscr.getch()
        if ch == ord('\n'):
            target_temperature = input_str
            if target_temperature.lower() == "stop":
                print("Stopping")
                break
            else:
                try:
                    target_temperature = int(target_temperature)
                    print("Setting standard temperature to {}".format(target_temperature))
                except ValueError:
                    stdscr.addstr(curses.LINES - 2, 0, "Invalid input")

            input_str = ""
        elif ch == curses.KEY_BACKSPACE or ch == 127:
            input_str = input_str[:-1]
        elif ch != -1:
            input_str += chr(ch)
        
        time.sleep(0.5)
        
        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)