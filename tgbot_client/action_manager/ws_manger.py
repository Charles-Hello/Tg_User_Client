
"""
这里将ws收到的message分类处理
"""
import re
from inspect import iscoroutinefunction
from pathlib import Path
from typing import Callable, Generic, Optional, ParamSpec, TypeVar
from .user_type import  TgUserType,StandAction
from .data import result_queue
import json
from datetime import datetime, timezone
E = TypeVar("E", bound=Optional[bool])
P = ParamSpec("P")

HANDLE_DICT: dict[str, Callable[P, E]] = {}
"""消息处理器字典"""

class MyBot:
  """
  定义抽象类型
  """
  ...

def add_handler(_tpye: str) -> Callable[P, E]:
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
    处理ACTION消息处理器
    """

    def __init__(self,bot:MyBot) -> None:
        self.bot = bot

    async def message_to_event(self, data: dict) ->E:
        """
        处理消息，返回事件
        """
        Functionname = data['function']
        handler = HANDLE_DICT.get(Functionname)
        if handler is None:
            return None
        if iscoroutinefunction(handler):
            result = await handler(self, data)
        else:
            result = handler(self, data)
        return result

    @add_handler(StandAction.GET_USERINFO)
    async def handle_text(self,msg:dict) -> E:
        """
        获取个人id
        """
        me = await self.bot.client.get_me()
        # 使用正则表达式匹配键值对
        pattern = r"(\w+)=(.*?)(?:, |$)"
        matches = re.findall(pattern, str(me))

        # 构建字典
        parsed_dict = {}
        for key, value in matches:
            if value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            elif value.startswith("b'") and value.endswith("'"):
                value = bytes.fromhex(value[2:-1]).decode('latin1')
            elif value == "True":
                value = True
            elif value == "False":
                value = False
            elif value == "None":
                value = None
            elif value.startswith("datetime.datetime("):
                datetime_parts = re.findall(r"\d+", value)
                value = datetime(
                    year=int(datetime_parts[0]),
                    month=int(datetime_parts[1]),
                    day=int(datetime_parts[2]),
                    hour=int(datetime_parts[3]),
                    minute=int(datetime_parts[4]),
                    second=int(datetime_parts[5]),
                    tzinfo=timezone.utc
                )
            parsed_dict[key] = value
        parsed_dict['user_id'] = parsed_dict.pop('id')
        parsed_dict['user_id'] = self.bot.client._self_id
        result_queue.put(parsed_dict)




    @add_handler(StandAction.GET_ID_INFO)
    async def handle_text(self,msg:dict) -> E:
        """
        获取个人id
        """
        from telethon.tl.types import PeerUser, PeerChat, PeerChannel

        # my_user    = await client.get_entity(PeerUser(some_id))
        # my_chat    = await client.get_entity(PeerChat(some_id))
        my_channel = await self.bot.client.get_entity(PeerUser(msg['wxid']))
        # entity = await self.bot.client.get_entity(msg['wxid'])
        print(my_channel.stringify())
        result_queue.put(str(my_channel))



    @add_handler(TgUserType.TEXT_MSG)
    async def handle_text(self, msg: dict) -> E:
        """
        处理文本
        """
        await self.bot.client.send_message(msg['wxid'], msg['message'])
        return True
      
    
    @add_handler(TgUserType.IMAGE_MSG)
    async def handle_file(self, msg: dict) -> E:
        """
        处理文件
        """
        await self.bot.client.send_file(msg['wxid'], msg['file'])
        return True
