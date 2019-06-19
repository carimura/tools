from fdk import response
import json
import os
import sys
import ujson
import time
import io
import asyncio
import slack

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")

sc = slack.WebClient(SLACK_TOKEN, run_async=True)

async def post_image_to_slack(msg, image_url):
    res = await sc.chat_postMessage(
        channel=SLACK_CHANNEL,
        text=msg,
        attachments=ujson.dumps([{"title": "", "image_url": image_url}]))
    return res

async def post_msg_to_slack(msg):
    res = await sc.chat_postMessage(
        channel=SLACK_CHANNEL,
        text=msg)
    return res

async def handler(ctx, data: io.BytesIO=None, loop=None):
    if data is not None or len(data) != 0:
        data = ujson.loads(data.getvalue())
        sys.stderr.write("payload to post-to-slack: {0}\n".format(ujson.dumps(data)))
        msg = data.get("msg")

    if not msg:
        msg = "Muy Guapo!"

    if not data.get("image_url"):
        res = await post_msg_to_slack(msg)
    else:
        res = await post_image_to_slack(msg, data.get("image_url"))
    
    return response.Response(
        ctx, status_code=200, response_data=json.dumps(
            {"ok": True}
        ),
        headers={"Content-Type": "application/json"}
    )
    #return res