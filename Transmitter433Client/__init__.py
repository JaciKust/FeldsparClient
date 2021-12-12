import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from FhaDataObjects.DataObjectButtonPressed import DataObjectButtonPressed
from Transmitter433Client.Transmitter433 import Transmitter433


from ControlPanelClient import ButtonColorSet
from ControlPanelClient.ControlPanelButton import ControlPanelButton

from RPi import GPIO
import time
import logging
from FhaMessageBus.MessageBus import MessageBus
from FhaCommon.Utility import JsonConfigurationReader
from ControlPanelClient.ControlPanel import ControlPanel

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class Runner:
    def __init__(self):
        logging.info('starting')

        mb_config = JsonConfigurationReader.default_reader.read('LightServer')
        self.message_bus = MessageBus(
            outgoing_ip="192.168.0.100", #mb_config.outgoing_ip,
            incoming_ip="192.168.0.158", #mb_config.incoming_ip,
            incoming_port="5555",#mb_config.incoming_port,
            outgoing_port="5556",#mb_config.outgoing_port,
            request_timeout=mb_config.request_timeout,
            request_retries=mb_config.request_retries,
            topic='Transmitter443' # topic
        )

        self.message_bus.server_events.on_message_receive += self.on_server_receive

    def _send_button_click_to_server(self, name, group, category, trigger_pin, button_press_time, control_panel_name):
        button_click_event = DataObjectButtonPressed(
            name,
            group,
            category,
            trigger_pin,
            button_press_time
        )
        self.message_bus.send(button_click_event)

    def on_server_receive(self, data):
        print("Received")
        #for command in data:
        if data.Name == 'DataObjectTransmitterCode':
            transmitter = Transmitter433()
            transmitter.send(data)


if __name__ == '__main__':
    Runner()

    while True:
        time.sleep(1)

