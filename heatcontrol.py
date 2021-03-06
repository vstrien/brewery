import RPi.GPIO as IO
import re, os, time

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

# define paths to 1-wire sensor data
paths = {
  "heatelement": "/sys/bus/w1/devices/28-3c01d0750556/w1_slave",
  "tube": "/sys/bus/w1/devices/28-3c01d075553b/w1_slave"
}

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(18, IO.OUT) # Pin 12 is GPIO 18

# channel, frequency in Hz 
# 0.5 = once every two seconds
p = IO.PWM(18, 10)


# Sensors id's
# 28-3c01d0750556  
# 28-3c01d075553b

for element in paths:
    print("{}: {}".format(element, read_sensor(paths[element])))

## Wat er moet gebeuren:
doeltemp = int(input("Gewenste temperatuur (C):\n"))
max_temp = int(input("Maximale temperatuur op verwarmingselement (C):\n"))
minutes_to_cook = int(input("Aantal minuten dat doeltemperatuur aangehouden moet worden:\n"))

print("[Opwarmen] start")

dutycycle = 50
olddutycycle = 50
p.start(dutycycle)
tubetemp = read_sensor(paths["tube"])
elemtemp = read_sensor(paths["heatelement"])

while tubetemp < doeltemp:
    olddutycycle = dutycycle
    if elemtemp < max_temp:
        dutycycle = min(dutycycle + 2, 100)
    else:
        dutycycle = max(dutycycle - 10, 0)
    if olddutycycle != dutycycle:
        print("[Opwarmen] wijzig duty cycle naar {}".format(dutycycle))
        p.ChangeDutyCycle(dutycycle)
    print("[Opwarmen] Tubetemp: {}".format(tubetemp))
    print("[Opwarmen] Elemtemp: {}".format(elemtemp))
    tubetemp = read_sensor(paths["tube"])
    elemtemp = read_sensor(paths["heatelement"])

print("[Opwarmen] voltooid")


start_cooking_time = time.time()
end_cooking_time = time.time() + (int(minutes_to_cook) * 60)



print("[Koken] start")
while time.time() < end_cooking_time:
    olddutycycle = dutycycle
    if tubetemp < doeltemp and elemtemp < max_temp:
        dutycycle = min(dutycycle + 2, 100)
    else:
        # Als ofwel de doeltemp al bereikt is 
        # of het verwarmingselement wordt te warm
        # dan moet er altijd afgeschaald worden
        # Uitschakelen gaat vanzelf (dutycycle = 0)
        dutycycle = max(dutycycle - 10, 0)
    if olddutycycle != dutycycle:
        print("[Koken] wijzig duty cycle naar {}".format(dutycycle))
        p.ChangeDutyCycle(dutycycle)
    print("[Koken] Tubetemp: {}".format(tubetemp))
    print("[Koken] Elemtemp: {}".format(elemtemp))
    tubetemp = read_sensor(paths["tube"])
    elemtemp = read_sensor(paths["heatelement"])

print("[Koken] voltooid")

p.stop()

## WARMHOUDEN
## end_time = huidigetijd() + aantal_minuten_koken
## while huidigetijd() < aantal_minuten_koken:
##   if huidigetemp_in_buis < doeltemp or temp_op_sensor < doeltemp:
##     if temp_op_sensor < max_temp:
##       pwm puls verhogen (langere tijden aan)
##     else:
##       sensor uit
## 
## Doeltemperatuur instellen en maximale afwijking

## Temperatuur niet bereikt?
## Temperatuuropgang inzetten, maximaal vermogen

## Controleren of het element niet meer dan de maximale afwijking vertoont

## Bij bereiken temperatuur: timer starten
## Bij aflopen timer: nieuwe temperatuur vragen

