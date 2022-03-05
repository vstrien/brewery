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
        value = str(float(m.group(2)) / 1000.0)
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

## Wat er moet gebeuren:
doeltemp = input("Gewenste temperatuur (C):\n")
max_temp = input("Maximale temperatuur op verwarmingselement (C):\n")
minutes_to_cook = input("Aantal minuten dat doeltemperatuur aangehouden moet worden:\n")

print("[Opwarmen] start")

dutycycle = 50
olddutycycle = 50
p.start(dutycycle)
while read_sensor(paths["tube"]) < doeltemp:
    olddutycycle = dutycycle
    if read_sensor(paths["heatelement"]) < max_temp:
        dutycycle = min(dutycycle + 10, 100)
    else:
        dutycycle = max(dutycycle - 10, 100)
    if olddutycycle != dutycycle:
        print("[Opwarmen] wijzig duty cycle naar {}".format(dutycycle))
        p.ChangeDutyCycle(dutycycle)
    for sensor in paths:
        print("[Opwarmen] Temp {}: {}".format(sensor, read_sensor(paths[sensor])))
    time.sleep(3)

print("[Opwarmen] voltooid")
p.stop()

start_cooking_time = time.time()
end_cooking_time = time.time() + (int(minutes_to_cook) * 60)



print("[Koken] start")
while time.time() < end_cooking_time:
    olddutycycle = dutycycle
    if read_sensor(paths["tube"]) < doeltemp and read_sensor(paths["heatelement"]) < max_temp:
        dutycycle = min(dutycycle + 10, 100)
    else:
        # Als ofwel de doeltemp al bereikt is 
        # of het verwarmingselement wordt te warm
        # dan moet er altijd afgeschaald worden
        # Uitschakelen gaat vanzelf (dutycycle = 0)
        dutycycle = max(dutycycle - 10, 100)
    if olddutycycle != dutycycle:
        print("[Koken] wijzig duty cycle naar {}".format(dutycycle))
        p.ChangeDutyCycle(dutycycle)
    time.sleep(1)

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

