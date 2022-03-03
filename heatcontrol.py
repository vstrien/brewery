import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(19, IO.OUT)

# channel, frequency in Hz 
# 0.5 = once every two seconds
p = IO.PWM(19, 0.5) 

