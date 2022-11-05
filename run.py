import sys
import signal
import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('bot_name', default='slack-bot')
def start_slack_bot(bot_name):
    click.echo('Starting Slack bot')
    from workerbee.bots.slack import SlackBot
    slack = SlackBot(bot_name=bot_name)
    slack.start()

@cli.command()
def start_bridge():
    click.echo('Starting websocket bridge')
    from workerbee.bridge import Bridge
    bridge = Bridge()
    bridge.start()

@cli.command()
@click.argument('bot_name', default='k8s')
def start_kubernetes_bot(bot_name):
    click.echo('Starting Kubernetes bot')
    from workerbee.bots.kubernetes import KubernetesBot
    k8s = KubernetesBot(bot_name=bot_name)
    k8s.start()

@cli.command()
@click.argument('bot_name')
@click.argument('command', required=True, nargs=-1)
def run_command(bot_name, command):
    from workerbee.bridge import Command
    cmd = Command(bot_name)
    print(cmd.run(" ".join(command)))


if __name__ == "__main__":

    def signal_handler(sig, frame):
        print('[Ctrl+C] Exiting...')
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    cli()
