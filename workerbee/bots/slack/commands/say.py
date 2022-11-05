
class Say(object):
    def __init__(self, client):
        self.client = client

    def help(self):
        return """\t- `say`: make me say something in a channel I am member of ```say #chatops hi!```\n"""

    def run(self, payload):
        payload = payload.split(maxsplit=1)
        if len(payload) > 1:
            target_channel = payload[0]
            message = payload[1]
        else:
            return f"ERROR Unable to find channel and message in '{payload}'"
        if target_channel.startswith("#"):
            target_channel = target_channel[1:]
        response = self.client.conversations_list()
        for channel in response.data.get('channels', []):
            if not channel.get('is_member', False) or channel.get('is_im', True) or channel.get('is_mpim', True) or channel.get('is_group', True) or channel.get('is_private', True):
                continue
            if channel.get('name') == target_channel or channel.get('id') == target_channel:
                self.client.chat_postMessage(channel=channel.get('id'), text=message)
                return "SUCCESS Done!"
        return f"ERROR Channel '{target_channel}' does not exist or I am not a member of"
