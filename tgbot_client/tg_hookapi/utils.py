from fastapi import APIRouter, Query, Depends, HTTPException
from tgbot_client.config import Config
import websockets
import ujson
from functools import wraps


async def send_ws(text_dict):
    async with websockets.connect(
        "ws://" + Config().application_ws_host + ":" + Config().application_ws_port
    ) as websocket:
        await websocket.send(ujson.dumps(text_dict))  # 将字典转换为字符串再发送
