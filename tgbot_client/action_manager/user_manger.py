"""
这里将tguser收到的message解析为event
"""
import re
from inspect import iscoroutinefunction
from pathlib import Path
from typing import Callable, Generic, Optional, ParamSpec, TypeVar
from urllib.parse import unquote
from uuid import uuid4
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

from tgbot_client.file_manager import FileManager
from tgbot_client.onebot12 import Message, MessageSegment
from tgbot_client.onebot12.event import (
    BotSelf,
    Event,
    FriendIncreaseEvent,
    FriendRequestEvent,
    GetGroupAnnouncementNotice,
    GetGroupCardNotice,
    GetGroupFileNotice,
    GetGroupPokeNotice,
    GetGroupRedBagNotice,
    GetPrivateCardNotice,
    GetPrivateFileNotice,
    GetPrivatePokeNotice,
    GetPrivateRedBagNotice,
    GroupMessageDeleteEvent,
    GroupMessageEvent,
    PrivateMessageDeleteEvent,
    PrivateMessageEvent,
)

from .model import Message as TgchatMessage
from .type import AppType, SysmsgType, WxType

E = TypeVar("E", bound=Event)
P = ParamSpec("P")

HANDLE_DICT: dict[int, Callable[P, E]] = {}
"""消息处理器字典"""
APP_HANDLERS: dict[int, Callable[P, Optional[E]]] = {}
"""app消息处理函数字典"""
SYS_MSG_HANDLERS: dict[str, Callable[P, Optional[E]]] = {}
"""系统消息处理函数字典"""
SYS_NOTICE_HANDLERS: list[Callable[P, Optional[E]]] = []
"""系统通知处理函数列表"""


def add_handler(_tpye: int) -> Callable[P, E]:
    """
    添加消息处理器
    """

    def _handle(func: Callable[P, E]) -> Callable[P, E]:
        global HANDLE_DICT
        HANDLE_DICT[_tpye] = func
        return func

    return _handle


class MessageHandler(Generic[E]):
    """
    TG消息处理器
    """

    image_path: Path
    """图片文件路径"""
    voice_path: Path
    """语音文件路径"""
    tgchat_path: Path
    """TG文件路径"""
    file_manager: FileManager
    """文件处理器"""

    def __init__(
        self,
        image_path: Path,
        voice_path: Path,
        tgchat_path: Path,
        file_manager: FileManager,
    ) -> None:
        self.image_path = image_path
        self.voice_path = voice_path
        self.tgchat_path = tgchat_path
        self.file_manager = file_manager

    async def message_to_event(self, msg: TgchatMessage) -> Optional[E]:
        """
        处理消息，返回事件
        """
        _type = msg.type
        handler = HANDLE_DICT.get(_type)
        if handler is None:
            return None
        if iscoroutinefunction(handler):
            result = await handler(self, msg)
        else:
            result = handler(self, msg)
        return result

    @add_handler(WxType.TEXT_MSG)
    def handle_text(self, msg: TgchatMessage) -> E:
        """
        处理文本
        """
        # 获取at
        raw_xml = msg.extrainfo

        if raw_xml:
            xml_obj = ET.fromstring(raw_xml)
            at_xml = xml_obj.find("./atuserlist")
        else:
            at_xml = None
        event_id = str(uuid4())

        # 向onebotv12是否自我发送
        if msg.isSendMsg:
            isSendMsg = True
        else:
            isSendMsg = False
        if at_xml is None:
            # 没有at
            # 获取message
            message = Message(MessageSegment.text(msg.message))
            # 判断群聊还是私聊
            if msg.isgroup or msg.ischannel:
                return GroupMessageEvent(
                    id=event_id,
                    time=msg.timestamp,
                    self=BotSelf(user_id=msg.self),
                    message_id=str(msg.msgid),
                    message=message,
                    alt_message=str(message),
                    user_id=msg.wxid,
                    group_id=msg.sender,
                    isSendMsg=isSendMsg,
                )
            return PrivateMessageEvent(
                id=event_id,
                time=msg.timestamp,
                self=BotSelf(user_id=msg.self),
                message_id=str(msg.msgid),
                message=message,
                alt_message=str(message),
                user_id=msg.wxid,
                isSendMsg=isSendMsg,
            )
