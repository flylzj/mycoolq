import nonebot
from fastapi import FastAPI, Form
from typing import Union
import base64
from pydantic import BaseModel

from coolq.util.coolq import send_message


class CheckchanCallbackModel(BaseModel):
    id_: Union[str, None] = None
    url: Union[str, None] = None
    value: Union[str, None] = None
    html: Union[str, None] = None
    link: Union[str, None] = None
    data: Union[bool, None] = None



img_dir = "/data/download"

app: FastAPI = nonebot.get_app()


@app.get("/msg")
async def send_msg(qq: str="", msg: str=""):
    if not qq or not msg:
        return {}
    msg = base64.b64decode(msg).decode()
    await send_message(message_type="private", recipient_id=qq, message=msg)
    return {}


@app.post("/checkchan/callback/{recipient_id}")
async def checkchan_callback(
        recipient_id: str,
        id: str= Form(""),
        url: str= Form(""),
        value: str= Form(""),
        html: str= Form(""),
        link: str= Form("")
    ):

    msg = f"检测任务有新的通知\n" \
          f"值: {value}\n" \
          f"链接: {link}"
    await send_message(message_type="private", recipient_id=recipient_id, message=msg)


@app.post("/emqx/callback/{recipient_id}")
async def checkchan_callback(
        recipient_id: str,
        id: str= Form(""),
        url: str= Form(""),
        value: str= Form(""),
        html: str= Form(""),
        link: str= Form("")
    ):

    msg = f"检测任务有新的通知\n" \
          f"值: {value}\n" \
          f"链接: {link}"
    await send_message(message_type="private", recipient_id=recipient_id, message=msg)



@app.get("/img") 
async def get_img(image_name):
    return 
    