"""
Continuous heat control for the brewery.
After entering the desired temperature and cook time, the program will keep this in the background.
This allows the operator to change the temperature at any given time.
"""

from HeatContoller import HeatController

# Load settings
import configparser
config = configparser.ConfigParser()
config.read('settings.ini')

heatelement = config['devices']['heatelement']
tube = config['devices']['tube']

hc = HeatController(tube, heatelement)

# Get user input
while True:
    print("Current temperature (tube) " + str(hc.tubetemp) + " C")
    print("Current temperature (elem) " + str(hc.elemtemp) + " C")
    print("Enter the desired temperature (C):")
    print("Enter STOP to stop the program")
    target_temperature = input("Enter the desired temperature (C):\n")
    if target_temperature.lower == "stop":
        hc.stop()
        break
    else:
        try:
            target_temperature = int(target_temperature)
            hc.setTargetTemperature(target_temperature)
        except ValueError:
            print("Invalid input")
            continue

