# WorkerBee

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Bridge

The `bridge` is a websocket server running on the specified `hostname` and `port` that allows inter-bot communication (connection protected by `username` and `password`). It can be started as follows:

```bash
export BRIDGE_USERNAME="bot"
export BRIDGE_PASSWORD="pw"
export BRIDGE_HOSTNAME="localhost"
export BRIDGE_PORT="8765"
python run.py start-bridge
```

## Kubernetes Bot

The kubernetes bot requires access to the `kubectl` executable, as well as permission to get information from a default Kubernetes cluster. It will connect to the specified `bridge` using the given credentials via environment variables, where it will be registered with the name `k8s`:

```bash
export BRIDGE_USERNAME="bot"
export BRIDGE_PASSWORD="pw"
export BRIDGE_HOSTNAME="localhost"
export BRIDGE_PORT="8765"
python run.py start-kubernetes-bot k8s
```

## Slack Bot

The Slack bot (named `WorkerBee` in Slack) requires bot + app tokens (it runs in Socket Mode, thus it does not require an open port for Slack to callback). It will connect slack, as well as to the specified `bridge` using the given credentials via environment variables, where it will be registered with the name `slack-bot`:

```bash
export SLACK_APP_TOKEN="xapp-..."
export SLACK_BOT_TOKEN="xoxb-..."
export BRIDGE_USERNAME="bot"
export BRIDGE_PASSWORD="pw"
export BRIDGE_HOSTNAME="localhost"
export BRIDGE_PORT="8765"
python run.py start-slack-bot slack-bot
```

It is possible to interact with the Slack bot via the Slack channels where it is member of (or directly via private messages). It is recommended to try `@WorkerBee help` to access the available commands. The Slack bot will use the `bridge` to proxy commands to other registered bots by using Slack messages with the pattern `@WorkerBee bot_name command arguments`.


## Command Line Interface

The command line interface can be used to run commands and print the results to the standard output:

```bash
export SLACK_APP_TOKEN="xapp-..."
export SLACK_BOT_TOKEN="xoxb-..."
export BRIDGE_USERNAME="bot"
export BRIDGE_PASSWORD="pw"
export BRIDGE_HOSTNAME="localhost"
export BRIDGE_PORT="8765"
python run.py run-command bridge list
```

Some examples:

- `python run.py run-command bridge list`: List all the registered bots in the `bridge`.
- `python run.py run-command slack-bot help`: Ask `slack-bot` to run the `help` command, which will collect also `help` instructions from all registered bots in the `bridge`.
- `python run.py run-command slack-bot say \#test Hello everybody! :wave:`: Ask `slack-bot` to say something in a channel (the bot needs to be member of).
- `python run.py run-command k8s show ads-dev ads-qa ads-prod`: Ask `k8s` bot to run the `show` command on the listed namespaces.

-
