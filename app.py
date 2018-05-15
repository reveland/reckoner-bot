import os
import sys
import json
from datetime import datetime
from threading import Timer
import urllib2
import flask
import requests
from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.keyboard_message import KeyboardMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

from messenger import Messenger

messenger = Messenger()

app = Flask(__name__)

bot_configuration = BotConfiguration(
    name='Reckoner',
    avatar='http://viber.com/avatar.jpg',
    auth_token='47ae7c0b0d27d1ef-2fe58f2b05086cfb-8a87db5e8dd49f97'
)
viber = Api(bot_configuration)

@app.route('/viber_bot', methods=['POST'])
def incoming():
    log("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        message_out = messenger.handle_messages(message.text)
        keyboard_string = '''{
            "Type": "keyboard",
            "Buttons": [{
                "Columns": 2,
                "Rows": 2,
                "Text": "<br><font color=\\"#494E67\\"><b>RENT</b></font>",
                "TextSize": "large",
                "TextHAlign": "center",
                "TextVAlign": "middle",
                "ActionType": "reply",
                "ActionBody": "RENT",
                "BgColor": "#f4dfc1",
                "BgMedia": "https://s3.amazonaws.com/splitwise/uploads/category/icon/slim/home/rent.png"
            },{
                "Columns": 2,
                "Rows": 2,
                "Text": "<br><font color=\\"#494E67\\"><b>WATER</b></font>",
                "TextSize": "large",
                "TextHAlign": "center",
                "TextVAlign": "middle",
                "ActionType": "reply",
                "ActionBody": "WATER",
                "BgColor": "#cee8f1",
                "BgMedia": "https://s3.amazonaws.com/splitwise/uploads/category/icon/slim/utilities/water.png"
            },{
                "Columns": 2,
                "Rows": 2,
                "Text": "<br><font color=\\"#494E67\\"><b>GAS</b></font>",
                "TextSize": "large",
                "TextHAlign": "center",
                "TextVAlign": "middle",
                "ActionType": "reply",
                "ActionBody": "GAS",
                "BgColor": "#cee8f1",
                "BgMedia": "https://s3.amazonaws.com/splitwise/uploads/category/icon/slim/utilities/heat-gas.png"
            },{
                "Columns": 2,
                "Rows": 2,
                "Text": "<br><font color=\\"#494E67\\"><b>INTERNET</b></font>",
                "TextSize": "large",
                "TextHAlign": "center",
                "TextVAlign": "middle",
                "ActionType": "reply",
                "ActionBody": "INTERNET",
                "BgColor": "#cee8f1",
                "BgMedia": "https://s3.amazonaws.com/splitwise/uploads/category/icon/slim/utilities/tv-phone-internet.png"
            },{
                "Columns": 2,
                "Rows": 2,
                "Text": "<br><font color=\\"#494E67\\"><b>ELECTRICITY</b></font>",
                "TextSize": "large",
                "TextHAlign": "center",
                "TextVAlign": "middle",
                "ActionType": "reply",
                "ActionBody": "ELECTRICITY",
                "BgColor": "#cee8f1",
                "BgMedia": "https://s3.amazonaws.com/splitwise/uploads/category/icon/slim/utilities/electricity.png"
            }]
        }'''
        keyboard = json.loads(keyboard_string)
        message_keyboard = KeyboardMessage(tracking_data=None, keyboard=keyboard)
        viber.send_messages(viber_request.sender.id, [
            TextMessage(text=message_out),
            message_keyboard
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    if 'text' in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]  # the message's text
                    else:
                        message_text = 'get_residents'
                    
                    message_text_out = messenger.handle_messages(message_text)
                    print(message_text_out)
                    send_message(sender_id, message_text_out)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def send_message(recipient_id, message_text):

    log(message_text)

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = str(msg)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug=True)
