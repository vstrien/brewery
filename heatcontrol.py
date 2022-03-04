import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(11, IO.OUT)

# channel, frequency in Hz 
# 0.5 = once every two seconds
p = IO.PWM(11, 0.5) 




## Wat er moet gebeuren:

## vraag om input: temperatuur
## vraag om input: maximale afwijking
## Tijd op deze temperatuur: aantal minuten

## OPWARMEN VOORAF
## while huidigetemp_in_buis < doeltemp:
##   if temp_op_sensor < max_temp en nog niet volledig aan:
##     pwm puls verhogen (langere tijden aan)
##   else:
##     pwm puls verlagen (kortere tijden aan)

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

