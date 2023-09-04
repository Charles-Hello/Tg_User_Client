from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .type import WxType

#TODO类型有些定义模糊
class Message(BaseModel):
  
    """接收的消息"""
    extrainfo: str
    """额外信息"""
    filepath: Optional[str]
    """文件路径"""
    isSendMsg: bool
    """是否为自身发送"""
    message: str
    """消息内容"""
    msgid: int
    """消息id"""
    self: int
    """自身id"""
    sender_name:str
    """发送方名字"""
    sender: int
    """发送方id"""
    thumb_path: str
    """缩略图位置"""
    time: datetime
    """发送时间"""
    timestamp: int
    """时间戳"""
    type: WxType
    """消息类型"""
    wxid: int
    """wxid"""
    isgroup:bool
    """是否为群组消息"""
    group_id :str
    """群组与频道id共用"""
    ischannel:bool
    """是否为频道消息"""
