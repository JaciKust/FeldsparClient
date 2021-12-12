import threading
import time

from RPi import GPIO
from Transmitter433Client.Constants import Transmitter as TransmitterConstant


class TransmitterLock:
    is_locked = False


class Transmitter433:
    def __init__(self):
        GPIO.setup(TransmitterConstant.PIN, GPIO.OUT)

    def send(self, dataObjectTransmitterCode):
        threading.Thread(target=self._run, args=[dataObjectTransmitterCode, ]).start()

    def _run(self, dataObjectTransmitterCode):
        while TransmitterLock.is_locked:
            time.sleep(0.01)

        try:
            TransmitterLock.is_locked = True
            for i in range(10):
                for bit in dataObjectTransmitterCode.Code:
                    if int(bit) == GPIO.HIGH:
                        GPIO.output(TransmitterConstant.PIN, GPIO.HIGH)
                        time.sleep(float(dataObjectTransmitterCode.OneHighTime))
                        GPIO.output(TransmitterConstant.PIN, GPIO.LOW)
                        time.sleep(float(dataObjectTransmitterCode.OneLowTime))
                    else:
                        GPIO.output(TransmitterConstant.PIN, GPIO.HIGH)
                        time.sleep(dataObjectTransmitterCode.ZeroHighTime)
                        GPIO.output(TransmitterConstant.PIN, GPIO.LOW)
                        time.sleep(dataObjectTransmitterCode.ZeroLowTime)
                GPIO.output(TransmitterConstant.PIN, GPIO.LOW)
                time.sleep(dataObjectTransmitterCode.IntervalTime)
        finally:
            TransmitterLock.is_locked = False
