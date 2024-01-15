from slack_sdk import WebClient

SLACK_TOKEN = "xoxb-5622312647746-5634968381057-Pd7A0aLBJdxtC7xClYzTIdma"

client = WebClient(token=SLACK_TOKEN)


class Slack:

    def __init__(self):
        pass

    def send_message(self, channel, message):
        response = client.chat_postMessage(
        channel=channel,
        blocks=message
        )