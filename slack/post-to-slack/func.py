import fdk
import json
import slackclient
import os
import sys
import ujson
import time

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")


def post_image_to_slack(msg, image_url):
    sc = slackclient.SlackClient(SLACK_TOKEN)
    return sc.api_call(
        "chat.postMessage",
        channel=SLACK_CHANNEL,
        text=msg,
        attachments=ujson.dumps([{"title": "", "image_url": image_url}]))

def post_msg_to_slack(msg):
    sc = slackclient.SlackClient(SLACK_TOKEN)
    return sc.api_call(
        "chat.postMessage",
        channel=SLACK_CHANNEL,
        text=msg)

def handler(ctx, data=None, loop=None):
    if data is not None or len(data) != 0:
        data = ujson.loads(data)
        sys.stderr.write(
            "payload to post-to-slack: {0}\n".format(ujson.dumps(data)))
        msg = data.get("msg")

    if not msg:
        msg = "Muy Guapo!"

    if not data.get("image_url"):
        resp = post_msg_to_slack(msg)
    else:
        resp = post_image_to_slack(msg, data.get("image_url"))

    # if "ok" in resp and resp["ok"]:
    #     sys.stderr.write("Image {0} Posted to Slack\n".format(image_url))
    # else:
    #     if "headers" in resp:
    #         hs = resp["headers"]
    #         if "Retry-After" in hs:
    #             delay = int(resp["headers"]["Retry-After"])
    #             time.sleep(delay)
    #             post_image_to_slack("MUY GUAPO!", image_url)
    #         else:
    #             raise Exception(ujson.dumps(resp))

    return resp


if __name__ == "__main__":
    fdk.handle(handler)
