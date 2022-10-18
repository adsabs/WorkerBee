import sys
import signal
from workerbee import slack

if __name__ == "__main__":
    def signal_handler(sig, frame):
        print('[Ctrl+C] Exiting...')
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    slack.bot_handler.start()
