from slack_sdk import WebClient
import json

SLACK_TOKEN = json.load(open("slack_token.json", "r"))["token"]

client = WebClient(token=SLACK_TOKEN)


class Slack:

    def __init__(self):
        pass

    def send_message(self, channel, message):
        response = client.chat_postMessage(
        channel=channel,
        blocks=message
        )