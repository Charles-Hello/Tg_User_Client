import asyncio
from telethon.sync import TelegramClient, events
from tgbot_client.com_tgchat import MessageReporter
from telethon import TelegramClient, events, connection
import websockets
import threading
from tgbot_client.config import Config, Env
import asyncio
from tgbot_client.utils import logger_wrapper
from tgbot_client.create_qr import creat_qr
from .login_lock import login_lock
from .qrlogin import Auth
import os
import json
from .ws_manger import MessageHandler
from .hander_msg import event_handel
log = logger_wrapper("tguserclient")


async def handler(event):
    
    msg_json = await event_handel(event,bot)

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
        self.config = config
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
env = Env()

config = Config(_common_config=env.dict())
print(config)
bot = MyBot(config)
