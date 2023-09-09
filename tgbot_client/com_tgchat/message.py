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


def add_app_handler(_tpye: int) -> Callable[P, Optional[E]]:
    """
    添加app_handler
    """

    def _handle(func: Callable[P, Optional[E]]) -> Callable[P, Optional[E]]:
        global APP_HANDLERS
        APP_HANDLERS[_tpye] = func
        return func

    return _handle


def add_sys_msg_handler(_tpye: str) -> Callable[P, Optional[E]]:
    """添加系统消息处理器"""

    def _handle(func: Callable[P, Optional[E]]) -> Callable[P, Optional[E]]:
        global SYS_MSG_HANDLERS
        SYS_MSG_HANDLERS[_tpye] = func
        return func

    return _handle


def add_sys_notice_handler(func: Callable[P, Optional[E]]) -> Callable[P, Optional[E]]:
    """添加系统处理器"""
    global SYS_NOTICE_HANDLERS
    SYS_NOTICE_HANDLERS.append(func)
    return func


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
                    sendname=msg.sender_name,
                    user_id=msg.sender,
                    group_id=msg.group_id,
                    ischannel=msg.ischannel,
                    isSendMsg=isSendMsg,
                    reply_message=msg.reply_message,
                    reply_sender_id=msg.reply_sender_id
                )
            return PrivateMessageEvent(
                id=event_id,
                time=msg.timestamp,
                self=BotSelf(user_id=msg.self),
                message_id=str(msg.msgid),
                message=message,
                alt_message=str(message),
                sendname=msg.sender_name,
                user_id=msg.wxid,
                ischannel=msg.ischannel,
                isSendMsg=isSendMsg,
                reply_message=msg.reply_message,
                reply_sender_id=msg.reply_sender_id
            )

        # 获取at
        at_list = at_xml.text.split(",")
        if at_list[0] == "":
            # pcTG发消息at时，会多一个','
            at_list.pop(0)

        # 这里用正则分割文本，来制造消息段，可能会有bug
        regex = r"(@[^@\s]+\s)"
        msg_list = re.split(regex, msg.message)
        new_msg = Message()
        for index, one_msg in enumerate(msg_list):
            if re.search(regex, one_msg) is None:
                if one_msg == "":
                    continue
                new_msg.append(MessageSegment.text(one_msg))
            else:
                try:
                    at_one = at_list.pop(0)
                except IndexError:
                    # 这里已经没有at目标了
                    text = "".join(msg_list[index:])
                    new_msg.append(MessageSegment.text(text))
                    break
                if at_one == "notify@all":
                    new_msg.append(MessageSegment.mention_all())
                else:
                    new_msg.append(MessageSegment.mention(at_one))
        return GroupMessageEvent(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            message_id=str(msg.msgid),
            message=new_msg,
            alt_message=str(new_msg),
            user_id=msg.wxid,
            group_id=msg.sender,
            isSendMsg=isSendMsg,
        )

    @add_handler(WxType.IMAGE_MSG)
    async def handle_image(self, msg: TgchatMessage) -> E:
        """
        处理图片
        """
        if msg.isSendMsg:
            isSendMsg = True
        else:
            isSendMsg = False
        # TODO 杂乱
        # file_name = Path(msg.filepath).stem
        # # 找图片
        # file_path = f"{self.image_path.absolute()}/{file_name}"
        # file = await self.file_manager.wait_for_image(file_path)
        # if file is None:
        #     return None

        file_name = Path(msg.filepath).stem
        # file = f"{self.image_path.absolute()}/{file_name}"
        event_id = str(uuid4())
        # file_id = await self.file_manager.cache_file_id_from_path(
        #     file, file.name, copy=False
        # )
        file_id = await self.file_manager.cache_file_id_from_path(
            Path(msg.filepath), file_name, copy=False
        )
        if msg.message:
            message = Message(
                MessageSegment.image(file_id=file_id)
                + Message(MessageSegment.text(msg.message))
            )
        else:
            message = Message(MessageSegment.image(file_id=file_id))
        # 检测是否为群聊
        if msg.isgroup:
            return GroupMessageEvent(
                id=event_id,
                time=msg.timestamp,
                self=BotSelf(user_id=msg.self),
                message_id=str(msg.msgid),
                message=message,
                alt_message=str(message),
                user_id=msg.sender,
                group_id=msg.group_id,
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

    @add_handler(WxType.VOICE_MSG)
    async def handle_voice(self, msg: TgchatMessage) -> E:
        """
        处理语音
        """
        if msg.isSendMsg:
            isSendMsg = True
        else:
            isSendMsg = False
        file_name = msg.sign
        file = self.voice_path / f"{file_name}.amr"
        file = await self.file_manager.wait_for_file(file)
        if file is None:
            return None

        event_id = str(uuid4())
        file_id = await self.file_manager.cache_file_id_from_path(
            file, file.name, copy=False
        )
        message = Message(MessageSegment.image(file_id=file_id))
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
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

    @add_handler(WxType.FRIEND_REQUEST)
    def handle_friend_request(self, msg: TgchatMessage) -> E:
        """
        处理好友请求
        """
        event_id = str(uuid4())
        raw_xml = msg.message
        xml_obj = ET.fromstring(raw_xml)
        attrib = xml_obj.attrib
        return FriendRequestEvent(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            user_id=attrib["fromusername"],
            v3=attrib["encryptusername"],
            v4=attrib["ticket"],
            nickname=attrib["fromnickname"],
            content=attrib["content"],
            country=attrib["country"],
            province=attrib["province"],
            city=attrib["city"],
        )

    @add_handler(WxType.CARD_MSG)
    def handle_card(self, msg: TgchatMessage) -> E:
        """
        处理名片消息
        """
        event_id = str(uuid4())
        raw_xml = msg.message
        xml_obj = ET.fromstring(raw_xml)
        attrib = xml_obj.attrib
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
            return GetGroupCardNotice(
                id=event_id,
                time=msg.timestamp,
                self=BotSelf(user_id=msg.self),
                user_id=msg.wxid,
                group_id=msg.sender,
                v3=attrib["username"],
                v4=attrib["antispamticket"],
                head_url=attrib["bigheadimgurl"],
                province=attrib["province"],
                city=attrib["city"],
                sex=attrib["sex"],
            )
        return GetPrivateCardNotice(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            user_id=msg.wxid,
            v3=attrib["username"],
            v4=attrib["antispamticket"],
            head_url=attrib["bigheadimgurl"],
            province=attrib["province"],
            city=attrib["city"],
            sex=attrib["sex"],
        )

    @add_handler(WxType.VIDEO_MSG)
    async def handle_video(self, msg: TgchatMessage) -> E:
        """
        处理视频
        """
        if msg.isSendMsg:
            isSendMsg = True
        else:
            isSendMsg = False
        video_img = self.tgchat_path / msg.thumb_path
        video_path = video_img.parent
        video_name = f"{video_img.stem}.mp4"
        video = video_path / video_name
        file = await self.file_manager.wait_for_file(video)
        if file is None:
            return None

        event_id = str(uuid4())
        file_id = await self.file_manager.cache_file_id_from_path(
            file, video_name, copy=False
        )
        message = Message(MessageSegment.video(file_id=file_id))
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
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

    @add_handler(WxType.EMOJI_MSG)
    async def handle_emoji(self, msg: TgchatMessage) -> E:
        """
        处理gif表情
        """
        if msg.isSendMsg:
            isSendMsg = True
        else:
            isSendMsg = False
        event_id = str(uuid4())
        # 获取文件名
        raw_xml = msg.message
        xml_obj = ET.fromstring(raw_xml)
        emoji_url = xml_obj.find("./emoji").attrib.get("cdnurl")
        emoji = unquote(emoji_url)
        file_id = await self.file_manager.cache_file_id_from_url(
            emoji, f"{msg.msgid}.gif"
        )
        message = Message(MessageSegment.emoji(file_id=file_id))
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
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

    @add_handler(WxType.LOCATION_MSG)
    def handle_location(self, msg: TgchatMessage) -> E:
        """
        处理位置信息
        """
        if msg.isSendMsg:
            isSendMsg = True
        else:
            isSendMsg = False
        event_id = str(uuid4())
        raw_xml = msg.message
        xml_obj = ET.fromstring(raw_xml)
        attrib = xml_obj.attrib
        message = Message(
            MessageSegment.location(
                latitude=attrib["x"],
                longitude=attrib["y"],
                title=attrib["label"],
                content=attrib["poiname"],
            )
        )
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
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

    @add_handler(WxType.APP_MSG)
    async def handle_app(self, msg: TgchatMessage) -> Optional[E]:
        """
        处理app消息
        """
        raw_xml = msg.message
        xml_obj = ET.fromstring(raw_xml)
        app = xml_obj.find("./appmsg")
        _type = int(app.find("./type").text)
        # todo
        if _type == 36:
            _type = 33
        result = None
        handler = APP_HANDLERS.get(_type)
        if handler is None:
            return None
        if iscoroutinefunction(handler):
            result = await handler(AppMessageHandler, self, msg, app)
        else:
            result = handler(AppMessageHandler, self, msg, app)
        return result

    @add_handler(WxType.SYSTEM_NOTICE)
    def handle_sys_notice(self, msg: TgchatMessage) -> Optional[E]:
        """
        处理系统提示
        """
        result = None
        for handler in SYS_NOTICE_HANDLERS:
            result = handler(SysNoticeHandler, msg)
            if result is not None:
                break
        return result

    @add_handler(WxType.SYSTEM_MSG)
    def handle_group_sys(self, msg: TgchatMessage) -> Optional[E]:
        """
        处理系统消息
        """
        result = None
        raw_xml = msg.message
        xml_obj = ET.fromstring(raw_xml)
        notice_type = xml_obj.attrib["type"]
        handler = SYS_MSG_HANDLERS.get(notice_type)
        if handler is None:
            return None
        result = handler(SysMsgHandler, msg, xml_obj)
        return result


class AppMessageHandler(Generic[E]):
    """
    app消息处理器
    """

    @classmethod
    @add_app_handler(AppType.APP_LINK)
    async def handle_app_link(
        cls, msg_handler: MessageHandler, msg: TgchatMessage, app: Element
    ) -> E:
        """
        处理其他应用分享的链接
        """
        if msg.isSendMsg:
            isSendMsg = True
        else:
            isSendMsg = False
        event_id = str(uuid4())
        title = app.find("./title").text
        des = app.find("./des").text
        url = app.find("./url").text.replace(" ", "")
        image_path = msg.thumb_path
        file_id = None
        if image_path != "":
            image_path = f"{msg_handler.tgchat_path}/{image_path}"
            image_path = Path(image_path)
            file_id = await msg_handler.file_manager.cache_file_id_from_path(
                image_path, name=image_path.stem, copy=False
            )
        if file_id is None:
            file_id = ""
        message = Message(
            MessageSegment.link(title=title, des=des, url=url, file_id=file_id)
        )
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
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

    @classmethod
    @add_app_handler(AppType.LINK_MSG)
    async def handle_link(
        cls, msg_handler: MessageHandler, msg: TgchatMessage, app: Element
    ) -> E:
        """
        处理链接
        """
        if msg.isSendMsg:
            isSendMsg = True
        else:
            isSendMsg = False
        event_id = str(uuid4())
        title = app.find("./title").text
        des = app.find("./des").text
        url = app.find("./url").text.replace(" ", "")
        image_path = msg.filepath
        file_id = None
        if image_path != "":
            image_path = f"{msg_handler.tgchat_path}/{image_path}"
            image_path = Path(image_path)
            file_id = await msg_handler.file_manager.cache_file_id_from_path(
                image_path, name=image_path.stem, copy=False
            )
        if file_id is None:
            file_id = ""
        message = Message(
            MessageSegment.link(title=title, des=des, url=url, file_id=file_id)
        )
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
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

    @classmethod
    @add_app_handler(AppType.FILE_NOTICE)
    async def handle_file(
        cls, msg_handler: MessageHandler, msg: TgchatMessage, app: Element
    ) -> E:
        """
        处理文件消息
        """
        if msg.isSendMsg:
            isSendMsg = True
        else:
            isSendMsg = False
        event_id = str(uuid4())
        file_name = app.find("./title").text
        md5 = app.find("./md5").text
        appattach = app.find("./appattach")
        file_length = int(appattach.find("./totallen").text)
        # 判断是否为通知还是下载完成
        overwrite_newmsgid = appattach.find("./overwrite_newmsgid")
        if overwrite_newmsgid is None:
            # 通知事件
            # 检测是否为群聊
            if "@chatroom" in msg.sender:
                return GetGroupFileNotice(
                    id=event_id,
                    time=msg.timestamp,
                    self=BotSelf(user_id=msg.self),
                    user_id=msg.wxid,
                    group_id=msg.sender,
                    file_name=file_name,
                    file_length=file_length,
                    md5=md5,
                    isSendMsg=isSendMsg,
                )
            else:
                return GetPrivateFileNotice(
                    id=event_id,
                    time=msg.timestamp,
                    self=BotSelf(user_id=msg.self),
                    user_id=msg.wxid,
                    file_name=file_name,
                    file_length=file_length,
                    md5=md5,
                    isSendMsg=isSendMsg,
                )

        # 文件消息
        file = msg_handler.tgchat_path / msg.filepath
        file = await msg_handler.file_manager.wait_for_file(file)
        if file is None:
            return None

        file_id = await msg_handler.file_manager.cache_file_id_from_path(
            file, file_name, copy=False
        )
        message = Message(MessageSegment.file(file_id=file_id))
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
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

    @classmethod
    @add_app_handler(AppType.QUOTE)
    def handle_quote(
        cls, msg_handler: MessageHandler, msg: TgchatMessage, app: Element
    ) -> E:
        """
        处理引用
        """
        if msg.isSendMsg:
            isSendMsg = True
        else:
            isSendMsg = False
        event_id = str(uuid4())
        text = app.find("./title").text
        from_msgid = app.find("./refermsg/svrid").text
        from_user = app.find("./refermsg/fromusr").text
        message = MessageSegment.reply(
            message_id=from_msgid, user_id=from_user
        ) + MessageSegment.text(text)
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
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

    @classmethod
    @add_app_handler(AppType.APP)
    def handle_app(
        cls, msg_handler: MessageHandler, msg: TgchatMessage, app: Element
    ) -> E:
        """
        处理app消息
        """
        if msg.isSendMsg:
            isSendMsg = True
        else:
            isSendMsg = False
        event_id = str(uuid4())
        title = app.find("./title").text
        url = app.find("./url").text
        app_id = app.find("./weappinfo/username").text
        message = Message(MessageSegment.app(app_id, title, url))
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
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

    @classmethod
    @add_app_handler(AppType.GROUP_ANNOUNCEMENT)
    def handle_announcement(
        cls, msg_handler: MessageHandler, msg: TgchatMessage, app: Element
    ) -> E:
        """处理群公告"""
        event_id = str(uuid4())
        text = app.find("textannouncement").text
        return GetGroupAnnouncementNotice(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            group_id=msg.sender,
            user_id=msg.wxid,
            text=text,
        )

    @classmethod
    @add_app_handler(AppType.TRANSFER)
    def handle_transfer(
        cls, msg_handler: MessageHandler, msg: TgchatMessage, app: Element
    ) -> E:
        """
        处理转账消息
        """
        # 告辞
        return None


class SysMsgHandler(Generic[E]):
    """
    群系统消息处理器
    """

    @classmethod
    @add_sys_msg_handler(SysmsgType.REVOKE)
    def revoke(cls, msg: TgchatMessage, xml_obj: Element) -> Optional[E]:
        """撤回消息事件"""
        msg_obj = xml_obj.find("./revokemsg/newmsgid")
        event_id = str(uuid4())
        message_id = msg_obj.text
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
            return GroupMessageDeleteEvent(
                id=event_id,
                time=msg.timestamp,
                self=BotSelf(user_id=msg.self),
                message_id=message_id,
                group_id=msg.sender,
                user_id=msg.wxid,
                operator_id="",
            )
        return PrivateMessageDeleteEvent(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            message_id=message_id,
            user_id=msg.wxid,
        )

    @classmethod
    @add_sys_msg_handler(SysmsgType.ROOMTOOL)
    def room_tools_tips(cls, msg: TgchatMessage, xml_obj: Element) -> Optional[E]:
        """
        群提示
        """
        todo = xml_obj.find("./todo")
        if todo is None:
            return None
        title = todo.find("./title").text
        creator = todo.find("./creator").text
        # TODO: 未完成
        return None

    @classmethod
    @add_sys_msg_handler(SysmsgType.FUNCTIONMSG)
    def function_msg(cls, msg: TgchatMessage, xml_obj: Element) -> Optional[E]:
        """
        函数消息
        """
        return None

    @classmethod
    @add_sys_msg_handler(SysmsgType.PAT)
    def pat(cls, msg: TgchatMessage, xml_obj: Element) -> Optional[E]:
        """
        拍一拍
        """
        pat = xml_obj.find("./pat")
        from_user = pat.find("./fromusername").text
        to_user = pat.find("./pattedusername").text
        chatroom = pat.find("./chatusername").text
        event_id = str(uuid4())
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
            return GetGroupPokeNotice(
                id=event_id,
                time=msg.timestamp,
                self=BotSelf(user_id=msg.self),
                user_id=to_user,
                from_user_id=from_user,
                group_id=chatroom,
            )
        return GetPrivatePokeNotice(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            user_id=to_user,
            from_user_id=from_user,
        )


class SysNoticeHandler(Generic[E]):
    """
    系统提示处理器
    """

    @classmethod
    @add_sys_notice_handler
    def read_bag(cls, msg: TgchatMessage) -> Optional[E]:
        """"""
        if msg.message != "收到红包，请在手机上查看":
            return None
        event_id = str(uuid4())
        # 检测是否为群聊
        if "@chatroom" in msg.sender:
            return GetGroupRedBagNotice(
                id=event_id,
                time=msg.timestamp,
                self=BotSelf(user_id=msg.self),
                user_id=msg.wxid,
                group_id=msg.sender,
            )
        return GetPrivateRedBagNotice(
            id=event_id,
            time=msg.timestamp,
            self=BotSelf(user_id=msg.self),
            user_id=msg.wxid,
        )
