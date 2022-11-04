import sys
import signal
import click

@click.group()
def cli():
    pass

@cli.command()
def start_slack_bot():
    click.echo('Starting Slack bot')
    from workerbee.bots.slack import SlackBot
    c = SlackBot()
    c.start()

@cli.command()
def start_bridge():
    click.echo('Starting websocket bridge')
    from workerbee.bridge import Bridge
    bridge = Bridge()
    bridge.start()

#@cli.command()
#@click.argument('bot_name')
#def start_bridge_worker(bot_name):
    #from workerbee import websocket
    #websocket.start_bot(bot_name, websocket.print_callback)

@cli.command()
@click.argument('bot_name')
@click.argument('command', nargs=-1)
def run_command(bot_name, command):
    from workerbee.bridge import Command
    c = Command(bot_name)
    c.run(" ".join(command))


if __name__ == "__main__":

    def signal_handler(sig, frame):
        print('[Ctrl+C] Exiting...')
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    cli()
