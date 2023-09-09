import time
from pathlib import Path
from uuid import uuid4

from pydantic import ValidationError

from tgbot_client.action_manager import (
    ActionManager,
    ActionRequest,
    ActionResponse,
    WsActionRequest,
    WsActionResponse,
    check_action_params,
)
from tgbot_client.com_tgchat import Message, MessageHandler
from tgbot_client.config import Config
from tgbot_client.consts import FILE_CACHE
from tgbot_client.file_manager import FileManager
from tgbot_client.onebot12 import (
    BotSelf,
    BotStatus,
    Event,
    Status,
    StatusUpdateEvent,
)
from tgbot_client.typing import overrides
from tgbot_client.utils import logger_wrapper
from telethon import TelegramClient, events
from .adapter import Adapter
import asyncio
from tgbot_client.action_manager.bot_core import bot
from tgbot_client.action_manager.login_lock import login_lock

log = logger_wrapper("TgUser Manager")


class TgChatManager(Adapter):
    """
    TG客户端行为管理
    """

    self_id: int
    """自身TGid"""
    file_manager: FileManager
    """文件管理模块"""
    action_manager: ActionManager
    """api管理模块"""
    message_handler: MessageHandler
    """消息处理器"""
    login_lock = login_lock
    """登录锁"""

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.self_id = None
        self.message_handler = None
        self.action_manager = ActionManager()
        self.file_manager = FileManager()
        self.login_lock = login_lock

    async def init(self) -> None:
        """
        初始化tgchat管理端
        """

        await self.action_manager.init(self.file_manager, self.config)
        log("DEBUG", "<y>开始获取wxid...</y>")
        await self.login_lock.acquire_lock()
        countdown = 60
        log("INFO", "<y>开启登陆user倒计时...</y>")
        _speak = True
        if not self.config.tg_qrlogin:
            _speak = False
            log("INFO", f"<y>你有120秒的登录时间哦！请抓紧时间登录！！...</y>")
        while countdown > 0:
            if not self.login_lock.lock._locked:
                if bot.client._self_id is None:
                    raise Exception("ERROR", "<r>Tg—user获取失败...网络错误！！</r>")
                else:
                    self.self_id = bot.client._self_id
                    log("SUCCESS", "<y>TGuser登录成功...恭喜你！！</y>")
                    log(
                        "SUCCESS",
                        f"<y>这 {self.config.tgusername}.session 是你登录凭证哦，注意保管，别泄露！！方便以后迁移需要！！</y>",
                    )
                    break
            else:
                await asyncio.sleep(2)
                countdown -= 1
                if _speak:
                    log("INFO", f"<y>还剩{countdown *2}秒哦！请尽快登录！！...</y>")
        if countdown == 0:
            raise Exception("ERROR", "<r>Tg—user获取失败...网络错误！！</r>")

        # TODO 后期分流
        video_path = Path(f"./{FILE_CACHE}")
        cache_path = Path(f"./{FILE_CACHE}")
        image_path = cache_path / "image" / str(self.self_id)
        voice_path = cache_path / "voice" / str(self.self_id)
        self.create_files(image_path)
        self.create_files(voice_path)
        self.message_handler = MessageHandler(
            image_path, voice_path, video_path, self.file_manager
        )
        self.action_manager.register_message_handler(self.handle_msg)
        log("DEBUG", "<g>TGid获取成功...</g>")
        log("INFO", "<g>初始化完成，启动uvicorn...</g>")

    def create_files(self, directory_path):
        """
        检查并创建文件夹，如果文件夹不存在
        """
        if not directory_path.is_dir():
            directory_path.mkdir(parents=True, exist_ok=True)

    @overrides(Adapter)
    async def action_request(self, request: ActionRequest) -> ActionResponse:
        """
        发起action请求
        """
        # 验证action
        try:
            action_name, action_model = check_action_params(request)
        except TypeError:
            return ActionResponse(
                status="failed",
                retcode=10002,
                data=None,
                message=f"未实现的action: {request.action}",
            )
        except ValueError:
            return ActionResponse(
                status="failed",
                retcode=10003,
                data=None,
                message="Param参数错误",
            )
        # 调用api
        return await self.action_manager.request(action_name, action_model)

    @overrides(Adapter)
    def get_status_update_event(slef) -> StatusUpdateEvent:
        """
        获取状态更新事件
        """
        event_id = str(uuid4())
        botself = BotSelf(user_id=slef.self_id)
        botstatus = BotStatus(self=botself, online=True)
        return StatusUpdateEvent(
            id=event_id, time=time.time(), status=Status(good=True, bots=[botstatus])
        )

    @overrides(Adapter)
    async def action_ws_request(self, request: WsActionRequest) -> WsActionResponse:
        """
        处理ws请求
        """
        echo = request.echo
        response = await self.action_request(
            ActionRequest(action=request.action, params=request.params)
        )
        return WsActionResponse(echo=echo, **response.dict())

    async def handle_msg(self, msg: str) -> None:
        """
        消息处理函数
        """
        try:
            message = Message.parse_raw(msg)
        except ValidationError as e:
            log("ERROR", f"TG消息实例化失败:{e}")
            return
        await self.handle_evnt_msg(message)

    async def handle_evnt_msg(self, msg: Message) -> None:
        """
        处理event消息
        """
        try:
            event: Event = await self.message_handler.message_to_event(msg)
        except Exception as e:
            log("ERROR", f"生成事件出错:{e}")
            return
        if event is None:
            log("DEBUG", "未生成合适事件")
            return
        log("SUCCESS", f"生成事件<g>[{event.__repr_name__()}]</g>:{event.dict()}")
        await self.handle_event(event)
