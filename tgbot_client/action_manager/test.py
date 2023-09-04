import asyncio
from telethon.sync import TelegramClient, events
from tgbot_client.com_tgchat import MessageReporter
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import json
from .type import WxType
from telethon import TelegramClient, events, connection
import websockets
import threading
from tgbot_client.config import Config, WebsocketType
import asyncio
from tgbot_client.utils import logger_wrapper
from tgbot_client.create_qr import creat_qr
from .login_lock import login_lock
from .qrlogin import Auth
import os
from .ws_manger import MessageHandler
from pathlib import Path
from tgbot_client.consts import FILE_CACHE
from uuid import uuid4

log = logger_wrapper("tguserclient")


# TODO 从test中分离，并且对各种信息事件进行处理
async def handler(event):
    class_sender = await event.get_sender()
    # TODO 群组、私人、群聊分类
    if event.is_channel:
        isSendMsg = False
        sender_name = ""
        group_id = event.chat_id
        isgroup = False
        ischannel = True
    if event.is_group:
        isSendMsg = class_sender.is_self  # 是否为自己发送
        sender_name = class_sender.first_name  # 发送人的名字
        group_id = event.chat_id
        isgroup = True
        ischannel = False
    if event.is_private:
        isSendMsg = class_sender.is_self  # 是否为自己发送
        sender_name = class_sender.first_name  # 发送人的名字
        group_id = ""
        isgroup = False
        ischannel = False

    sender_id = int(class_sender.id)  # 发送人的id   测试id为1716089227，我的id为1123322058
    class_message = event.message
    if isSendMsg:
        sender_id = class_message.chat_id  # 如果是我发送，则是对方id
    message = class_message.message  # 发送的信息内容
    msgid = event._message_id  # 发送的信息的id
    selfid = int(event.client._self_id)
    time = class_message.date  # 发送的时间
    timestamp = int(time.timestamp())
    time_str = time.strftime("%Y-%m-%dT%H:%M:%S")
    Messagetype = WxType.TEXT_MSG
    file_name = ""
    if class_message.file:
        _pathName = Path(".") / FILE_CACHE / "image" / str(selfid)
        if class_message.file.name:
            file_name = _pathName / f"{class_message.file.name}"
        else:
            file_name = _pathName / f"{str(uuid4())}{class_message.file.ext}"
        await bot.client.download_media(class_message.file.media, file_name)
        Messagetype = WxType.IMAGE_MSG

    # TODO 对信息进行分类，文本，语言，图片等等
    msg_dict = {
        "extrainfo": "",
        "filepath": str(file_name),
        "isSendMsg": isSendMsg,
        "message": message,
        "msgid": msgid,
        "self": selfid,
        "sender_name": sender_name,
        "sender": sender_id,
        "thumb_path": "",
        "time": time_str,
        "timestamp": timestamp,
        "type": Messagetype,
        "wxid": sender_id,
        "isgroup": isgroup,
        "group_id": group_id,
        "ischannel": ischannel,
    }

    msg_json = json.dumps(msg_dict)

    MessageReporter().OnGetMessageEvent(msg_json)


async def websocket_handler(websocket):
    try:
        while True:
            message = await websocket.recv()
            data = json.loads(message)  # 解析接收到的数据，将字符串转换为字典
            try:
                await MessageHandler(bot).message_to_event(data)
            except Exception as e:
                log("ERROR", f"完成ws事件出错:{e}")
                return

    except websockets.ConnectionClosedOK:
        pass
    except json.JSONDecodeError:
        print("Failed to decode JSON data:", message)


class MyBot:
    def __init__(self, config: Config):
        self.username = config.tgusername
        self.config = Config()
        if config.tg_proxy:
            if config.tg_proxy_mode == "socks5":
                if not config.tg_proxy_user:
                    proxy = (
                        config.tg_proxy_mode,
                        config.tg_proxy_host,
                        config.tg_proxy_port,
                    )
                    self.client = TelegramClient(
                        self.username,
                        config.tg_api_id,
                        config.tg_api_hash,
                        proxy=proxy,
                        connection_retries=None,
                    )
                else:
                    proxy = (
                        config.tg_proxy_mode,
                        config.tg_proxy_host,
                        config.tg_proxy_port,
                        config.tg_proxy_user,
                        config.tg_proxy_pass,
                    )
                    self.client = TelegramClient(
                        self.username,
                        config.tg_api_id,
                        config.tg_api_hash,
                        proxy=proxy,
                        connection_retries=None,
                    )
            elif config.tg_proxy_mode == "MTProto":
                proxy = (
                    config.tg_proxy_host,
                    config.tg_proxy_port,
                    config.tg_proxy_pass,
                )
                self.client = TelegramClient(
                    self.username,
                    config.tg_api_id,
                    config.tg_api_hash,
                    proxy=proxy,
                    connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
                )
        else:
            self.client = TelegramClient(
                self.username,
                config.tg_api_id,
                config.tg_api_hash,
                connection_retries=None,
            )
        self.ws_host = config.application_ws_host
        self.ws_port = config.application_ws_port

    def thread_loop_task(self, loop):
        asyncio.set_event_loop(loop)

        async def client_start():
            try:
                _login_Status = False
                try:
                    log("INFO", f"<y>正在尝试为你自动登录....！！...</y>")
                    await asyncio.wait_for(self.client.connect(), timeout=5.0)
                except asyncio.TimeoutError:
                    log("ERROR", f"<y>TgUser超时连接!请尝试更换代理...然后再次运行本程序</y>")
                    os._exit(0)
                if self.client._self_id:
                    _login_Status = True
                if not _login_Status:
                    if self.config.tg_qrlogin:
                        qr_login = await self.client.qr_login()
                        countdown = 3
                        log(
                            "INFO",
                            f"<y>请前往 http://localhost:{self.config.tg_qrlogin_qrWeb_port} 扫码登陆！！...</y>",
                        )
                        if self.config.tg_qq_email_status:
                            log(
                                "INFO",
                                f"<y>请前往 {self.config.tg_qrlogin_qqemail}查看邮箱扫码登陆！！...</y>",
                            )
                            log(
                                "INFO",
                                f"<y>识别码是：{self.config.tg_qrlogin_qqemail_fakeStr}！！...</y>",
                            )
                        log("INFO", f"<y>请扫码登录！！...</y>")
                        creat_qr(qr_login.url)
                        Auth(
                            port=self.config.tg_qrlogin_qrWeb_port,
                            email=(
                                self.config.tg_qrlogin_qqemail,
                                self.config.tg_qrlogin_qqemail_fakeStr,
                            ),
                        )
                        while countdown > 0:
                            if self.client._self_id:
                                log("SUCCESS", f"<y>扫码成功！！...</y>")
                                break
                            else:
                                try:
                                    log("INFO", f"<y>等待30s...</y>")
                                    await qr_login.wait(30)
                                except asyncio.TimeoutError:
                                    await qr_login.recreate()
                                    creat_qr(qr_login.url)
                                    log("INFO", f"<y>二维码已经刷新...</y>")
                                    countdown -= 1
                                    log(
                                        "INFO",
                                        f"<y>还剩{countdown*30}秒哦！请尽快扫码登录！！...</y>",
                                    )
                        if countdown == 0:
                            raise Exception("ERROR", "<r>TGuser登陆失败...！！</r>")
                    else:
                        log(
                            "INFO", f"<y>正采用手机号码登陆：不国内外号码记得前缀例如 +8615344683200！！...</y>"
                        )
                        self.client = await self.client.start()

                # TODO 添加多个client类型/事件的监控
                self.client.add_event_handler(handler, events.NewMessage())
                run = self.client.run_until_disconnected()
                login_lock.unlock()
                start_server = websockets.serve(
                    websocket_handler, self.ws_host, self.ws_port
                )
                await asyncio.gather(run, start_server)

            except Exception as e:
                log("ERROR", f"<r>{e}</r>")

        future = asyncio.gather(client_start())
        loop.run_until_complete(future)

    async def _run(self):
        thread_loop = asyncio.new_event_loop()
        t = threading.Thread(target=self.thread_loop_task, args=(thread_loop,))
        t.daemon = True
        t.start()


# 创建 MyBot 实例
bot = MyBot(config=Config())
