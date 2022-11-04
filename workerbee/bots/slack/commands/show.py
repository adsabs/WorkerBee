from collections import defaultdict
from ....tools.k8s import Kubectl

class Show(object):
    def __init__(self):
        self.kubectl = Kubectl()
        self.fmt = "{:30}{:20}{:20}{:20}"

    def _parse_kubectl_get(self, json_output):
        """Convert JSON to list of deployment info"""
        deployments = []
        for deploy in json_output.get('items', []):
            deployments.append(
                {
                    'name': deploy.get('metadata', {}).get('name', None),
                    'namespace': deploy.get('metadata', {}).get('namespace', None),
                    'available': deploy.get('status', {}).get('availableReplicas', -1),
                    'ready': deploy.get('status', {}).get('readyReplicas', -1),
                    'image': deploy.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [{}])[0].get('image', None),
                }
            )
        deployments.sort(key=lambda x: x['name'])
        return deployments

    def _list_deployments(self, namespace):
        """ deploy/sts """
        if "solr" in namespace:
            item_type = "sts"
        else:
            item_type = "deploy"
        get_output = self.kubectl.get(item_type, namespace)
        deployments = self._parse_kubectl_get(get_output)
        return deployments

    def _format_deployment(self, requested_namespaces, deployment_name, deployments_information):
        out = {}
        out['name'] = deployment_name
        out['namespace'] = '|'.join(requested_namespaces)
        out['replicas'] = []
        out['images'] = []

        namespaces = [x['namespace'] for x in deployments_information]

        for namespace in requested_namespaces:
            try:
                idx = namespaces.index(namespace)
            except ValueError:
                out['replicas'].append('-:-')
                out['images'].append('-')
            else:
                out['replicas'].append('%s:%s' % (deployments_information[idx]['available'], deployments_information[idx]['ready']))
                out['images'].append(deployments_information[idx]['image'].split(':')[-1])

        out['replicas'] = '|'.join(out['replicas'])

        images = set(out['images'])
        if len(images) == 1:
            out['images'] = out['images'][0]
        else:
            out['images'] = '|'.join(out['images'])

        return self.fmt.format(*out.values())

    def run(self, namespaces):
        if len(namespaces) == 0:
            return "Missing arguments. Type `@WorkerBee help` for help."

        data = defaultdict(list)
        for namespace in namespaces:
            for deploy in self._list_deployments(namespace):
                name = deploy['name']
                data[name].append(deploy)

        deployments_show = []
        deployments_show.append(self.fmt.format('name', 'namespace(s)', 'alive:ready', 'image(s)'))
        for deployment_name, deployments_information in data.items():
            deployments_show.append(self._format_deployment(namespaces, deployment_name, deployments_information))

        return "```{}```".format("\n".join(deployments_show))

    def help(self):
        return """- `show`: list kubernetes deployments ```show ads-dev ads-qa ads-prod```\n"""

