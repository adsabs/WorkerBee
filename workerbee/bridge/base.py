import os
import sys

class BridgeBase(object):
    def __init__(self):
        try:
            self.bridge_password = os.environ['BRIDGE_PASSWORD']
        except KeyError:
            print("'BRIDGE_PASSWORD' needs to be defined as a environment variable")
            sys.exit(1)
        self.bridge_username = os.environ.get('BRIDGE_USERNAME', 'bot')
        self.bridge_hostname = os.environ.get('BRIDGE_HOSTNAME', 'localhost')
        self.bridge_port = os.environ.get('BRIDGE_PORT', '8765')

    def start(self):
        raise NotImplementedError

    def decompose(self, msg):
        leading = ''
        payload = ''
        splitted_msg = msg.split(maxsplit=1)
        if len(splitted_msg) > 0:
            leading = splitted_msg[0]
        if len(splitted_msg) > 1:
            payload = splitted_msg[1]
        return leading, payload
