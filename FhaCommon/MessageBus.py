import json
import string
from collections import namedtuple
import threading
import time
import zmq
import logging
import sys

from events import Events


class MessageBus:
    def __init__(self, outgoing_ip, incoming_ip, incoming_port, outgoing_port, request_timeout, request_retries):
        logging.info('Starting Message bus')

        self.outgoing_ip = outgoing_ip
        self.incoming_ip = incoming_ip
        self.incoming_port = incoming_port
        self.outgoing_port = outgoing_port
        self.request_timeout = request_timeout
        self.request_retries = request_retries

        self.context = zmq.Context()
        # self.incoming_socket = self.context.socket(zmq.SUB)
        # self.incoming_socket.connect(
        #     "tcp://{}:{}".format(
        #         '192.168.0.100',#self.outgoing_ip,
        #         '5555', #self.outgoing_port
        #     )
        # )
        #
        # #zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"
        # self.incoming_socket.setsockopt_string(zmq.SUBSCRIBE, 'A')

        self.incoming_socket = zmq.Context().socket(zmq.SUB)
        self.incoming_socket.connect("tcp://192.168.0.100:5557")
        self.incoming_socket.setsockopt_string(zmq.SUBSCRIBE, 'A')

        self.server_events = Events()
        self.socket_thread = threading.Thread(target=self.run_message_server)
        self.socket_thread.start()

    def __del__(self):
        self.continue_message_server = False

    def _decoder(self, dict):
        return namedtuple('X', dict.keys())(*dict.values())

    continue_message_server = True

    def run_message_server(self):
        try:
            while self.continue_message_server:
                #  Wait for next request from client
                message = self.incoming_socket.recv()
                if message != b"ack":
                    if message == b'A':
                        continue
                    logging.info("Received request: %s" % message)
                    # self.incoming_socket.send(b"ack")
                    print(message)
                    data = json.loads(message.decode('utf-8'), object_hook=self._decoder)
                    print("parsed " + str(data))
                    self.server_events.on_message_receive(data)
                    print("managed")
                time.sleep(0.2)
        except:
            print("damn")
        # def __init__(self):
        #     context = zmq.Context()
        #     socket = context.socket(zmq.SUB)
        #
        #     print("Collecting updates from weather server...")
        #     socket.connect("tcp://192.168.0.100:5556")
        #
        #     # Subscribe to zipcode, default is NYC, 10001
        #     zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"
        #     socket.setsockopt_string(
        #         zmq.SUBSCRIBE, 'A'
        #     )
        #
        #     # Process 5 updates
        #     total_temp = 0
        #     for update_nbr in range(5):
        #         string = socket.recv_string()
        #         zipcode, temperature, relhumidity = string.split()
        #         print("Recieved")
        #         total_temp += int(temperature)
        #
        #     print((f"Average temperature for zipcode "
        #            f"'{zip_filter}' was {total_temp / (update_nbr + 1)} F"))

    def send(self, data):
        print("Sending!!!! " + str(data))
        data = json.dumps(data.__dict__)
        logging.info("Connecting to server…")
        client = self.context.socket(zmq.REQ)
        print("Senting on ZMQ?E?")
        client.connect("tcp://{}:{}".format(self.outgoing_ip, self.outgoing_port))

        request = str(data).encode()
        #logging.info("Sending (%s)", request)
        client.send(request)

        retries_left = self.request_retries
        while True:
            if (client.poll(self.request_timeout) & zmq.POLLIN) != 0:
                reply = client.recv()
                if reply == b"ack":
                    logging.info("Server replied OK (%s)", reply)
                    break
                else:
                    logging.error("Malformed reply from server: %s", reply)
                    continue

            retries_left -= 1
            logging.warning("No response from server")
            # Socket is confused. Close and remove it.
            client.setsockopt(zmq.LINGER, 0)
            client.close()
            if retries_left == 0:
                logging.error("Server seems to be offline, abandoning")
                return

            logging.info("Reconnecting to server…")
            # Create new connection
            client = self.context.socket(zmq.REQ)
            client.connect("tcp://{}:{}".format(self.outgoing_ip, self.outgoing_port))
            logging.info("Resending (%s)", request)
            client.send(request)
