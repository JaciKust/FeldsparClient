import time

from RPi import GPIO

from FhaCommon.Interactable.Toggleable.Toggleable import Toggleable


class Relay(Toggleable):
    def __init__(self, database_id, pin, max_time_on=None):
        super().__init__(database_id, max_time_on)

        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def _execute_set_on(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.is_on = True

    def _execute_set_off(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.is_on = False

    def pulse(self):
        try:
            self.set_on()
            time.sleep(0.1)
        finally:
            self.set_off()
        self.set_off()
