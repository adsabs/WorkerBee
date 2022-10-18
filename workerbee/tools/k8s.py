import json
from subprocess import PIPE, Popen

class Kubectl(object):

    def get(self, item_type, namespace):
        """Run kubectl and parse JSON output"""
        shell_command="kubectl get {} -n {} -o json".format(item_type, namespace)
        p = Popen(shell_command, shell=True, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()

        json_output = {}
        if p.returncode == 0:
            try:
                json_output = json.loads(output)
            except json.JSONDecodeError:
                pass
        return json_output

