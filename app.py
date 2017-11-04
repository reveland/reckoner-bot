import os
import sys
import json
from datetime import datetime
from trello_kk import KoKa
from threading import Timer
import urllib2
from reckoner import RentReckoner
from rent_provider_trello import DataProvider

import flask
import requests
from flask import Flask, request

app = Flask(__name__)

KK = KoKa()

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
                    
                    send_message(sender_id, KK.handle_messages(message_text))

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

@APP.route("/habitations/<int:habitant_id>/residents/<int:resident_id>/dept")
def get_dept(habitant_id, resident_id):
    dept = "# %d #" % RENT_RECKONER.get_debt(
        habitant_id, DATA_PROVIDER.get_resident_by_id(habitant_id, resident_id))
    resp = flask.Response(dept)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@APP.route("/habitations/<int:habitant_id>/bills")
def get_bills(habitant_id):
    bills = json.dumps(RENT_RECKONER.get_bills_to_ui(
        habitant_id), default=lambda o: o.__dict__)
    resp = flask.Response(bills)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

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

def ping_fb_reckoner():
    print(urllib2.urlopen("https://limitless-stream-25117.herokuapp.com/").read())
    Timer(30, ping_fb_reckoner).start()

if __name__ == '__main__':
    Timer(30, ping_fb_reckoner).start()
    app.run(debug=True)
