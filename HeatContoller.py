import RPi.GPIO as IO
import re
import threading
import time

class HeatController:
  def __init__(self, tube_path, heat_path, target_temperature = 0, max_temperature = 0, GPIO_PIN = 18):
    IO.setwarnings(False)
    IO.setmode(IO.BCM)
    IO.setup(GPIO_PIN, IO.OUT) # Pin 12 is GPIO 18
    self.target_lock = threading.Lock()
    self.sensor_lock = threading.Lock()
    self.target_temperature = target_temperature
    self.max_temperature = max_temperature
    self.tubetemp = 0
    self.elemtemp = 0
    self.dutycycle = 0
    self.p = IO.PWM(18, 10)
    self.tube_path = tube_path
    self.heat_path = heat_path
    self.margin = 2 # Margin in degrees celcius
    self.is_started = False

  @staticmethod
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

  def updateSensorValues(self):
    with self.sensor_lock:
        self.tubetemp = HeatController.read_sensor(self.tube_path)
        self.elemtemp = HeatController.read_sensor(self.heat_path)

  def setTargetTemperature(self, target_temperature):
    with self.target_lock:
        self.target_temperature = target_temperature

  def setMaxTemperature(self, max_temperature):
    with self.target_lock:
        self.max_temperature = max_temperature

  def updateDutyCycle(self):
     self.updateSensorValues()
     current_max = max(self.tubetemp, self.elemtemp)
     with self.target_lock:
        if self.target_temperature < current_max - self.margin:
            # Below the allowed margin. Full power.
            self.dutycycle = 100
        elif self.target_temperature > current_max + self.margin:
            # Above the allowed margin. Turn off.
            self.dutycycle = 0
        else:
            # Between the allowed margin. Half power.
            # In the future, we could fine-tune this
            self.dutycycle = 50

  def updateDutyCycleDaemon(self, seconds_between_updates = 30):
    while True:
        self.updateDutyCycle()
        time.sleep(seconds_between_updates)

  def start(self):
    self.updateDutyCycle()
    p.start(self.dutycycle)

    # Start the update thread
    self.update_thread = threading.Thread(target=self.updateDutyCycleDaemon)
    self.update_thread.daemon = True
    self.update_thread.start()
    self.is_started = True

  def stop(self):
    p.stop()
    self.update_thread.join(timeout=0)
    self.is_started = False