import slack
import os
from pathlib import Path
from dotenv import load_dotenv
# Import Flask
from flask import Flask, request, Response
# Handles events from Slack
from slackeventsapi import SlackEventAdapter

import requests

import json


message_counts = {}
# Load the Token from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Configure your flask application
app = Flask(__name__)

# Configure SlackEventAdapter to handle events
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

# Using WebClient in slack, there are other clients built-in as well !!
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])


# connect the bot to the channel in Slack Channel
client.chat_postMessage(channel='#bot-testing', text='Send Message Demo')

# Get Bot ID
BOT_ID = client.api_call("auth.test")['user_id']


@slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text2 = event.get('text')

    if (text2 == 'toronto'):
        response = requests.get(
            'http://api.openweathermap.org/data/2.5/weather?q=toronto&appid=104fed0344bb1161f3581a56f08e5075')

        print(response.json())
        client.chat_postMessage(
            channel=channel_id, text=json.dumps(response.json()))

    if BOT_ID != user_id:
        # client.chat_postMessage(channel=channel_id, text=text2)
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1


@ app.route('/message-count', methods=['GET', 'POST'])
def message_count():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    # print(data)
    message_count = message_counts.get(user_id, 0)
    if message_count:
        client.chat_postMessage(
            channel=channel_id, text=f'Message:{message_count}')

    return Response(), 200


# handling Message Events


# Run the webserver micro-service
if __name__ == "__main__":
    app.run(debug=True)
