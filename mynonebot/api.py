import nonebot
from fastapi import FastAPI
from coolq.util.coolq import send_message
import base64


img_dir = "/data/download"

app: FastAPI = nonebot.get_app()


@app.get("/msg")
async def send_msg(qq: str="", msg: str=""):
    if not qq or not msg:
        return {}
    msg = base64.b64decode(msg).decode()
    await send_message(message_type="private", recipient_id=qq, message=msg)
    return {}


@app.get("/img") 
async def get_img(image_name):
    return 
    