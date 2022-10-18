# WorkerBee

This code requires access to the executable `kubectl` and permission to get information from a default Kubernetes cluster.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export SLACK_APP_TOKEN="xapp-..."
export SLACK_BOT_TOKEN="xoxb-..."
python run.py
```
