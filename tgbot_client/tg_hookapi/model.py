"""
构造ws对应的http请求
"""
from pydantic import BaseModel, root_validator
from .utils import send_ws
from typing import Annotated, Union
from pathlib import Path
from tgbot_client.action_manager.data import result_queue


class SendText(BaseModel):
    """
    description: 发送文本信息
    """

    function: str = "send_text"
    message: str = None
    wxid: int = None

    def __init__(self, message, wxid, function="send_text"):
        super().__init__(message=message, wxid=wxid, function=function)

    async def run(self):
        req_dict = {
            "function": self.function,
            "message": self.message,
            "wxid": self.wxid,
        }
        await send_ws(req_dict)


class Get_Self_Info(BaseModel):
    """
    description: 发送获取个人信息
    """

    function: str = "get_self_info"

    def __init__(self, function="get_self_info"):
        super().__init__(function=function)

    async def run(self):
        req_dict = {
            "function": self.function,
        }
        await send_ws(req_dict)
        return result_queue.get(timeout=3)


class Get_ID_Info(BaseModel):
    """
    description: 发送获取id信息
    """

    function: str = "get_id_info"
    wxid: int = None

    def __init__(self, wxid, function="get_id_info"):
        super().__init__(wxid=wxid, function=function)

    async def run(self):
        req_dict = {
            "function": self.function,
            "wxid": self.wxid,
        }
        await send_ws(req_dict)
        return result_queue.get(timeout=3)


class Sendfile(BaseModel):
    """
    description: 发送文件信息
    """

    function: str = "send_file"
    file: str = None
    wxid: int = None

    def __init__(self, file, wxid, function="send_file"):
        super().__init__(file=file, wxid=wxid, function=function)

    async def run(self):
        req_dict = {
            "function": self.function,
            "file": self.file,
            "wxid": self.wxid,
        }
        await send_ws(req_dict)


class Uploadfile(BaseModel):
    """
    description: 上传文件信息
    """

    type: str
    name: str
    magic: Union[str, bytes, Path]


class Deletmessage(BaseModel):
    """
    description: 删除信息
    """
    function="delete_message"
    chat_id :str
    message: str
    def __init__(self, chat_id,message, function="delete_message"):
            super().__init__(chat_id=chat_id,message=message, function=function)

    async def run(self):
        req_dict = {
            "function": self.function,
            "chat_id":self.chat_id,
            "message": self.message,
        }
        await send_ws(req_dict)
        
        
class Editmessage(BaseModel):
    """
    description: 编辑信息
    """
    function="edit_message"
    chat_id :str
    before_message: str
    after_message: str
    def __init__(self, chat_id,before_message,after_message, function="edit_message"):
            super().__init__(chat_id=chat_id,before_message=before_message, after_message=after_message,function=function)

    async def run(self):
        req_dict = {
            "function": self.function,
            "chat_id":self.chat_id,
            "before_message": self.before_message,
            "after_message": self.after_message,
        }
        await send_ws(req_dict)

def ApiManger(_type: str):
    """_summary_

    Args:
        _type1 (str): send_text,
        _type2 (str): send_file,
        _type3 (str): get_self_info
        _type4 (str): get_id_info
        _type5 (str): delete_message
        _type6 (str): edit_message

    Returns:
        _type_: fun_class
    """
    if _type == "send_text":
        return SendText
    elif _type == "get_self_info":
        return Get_Self_Info
    elif _type == "get_id_info":
        return Get_ID_Info
    elif _type == "send_file":
        return Sendfile
    elif _type == "upload_file":
        return Uploadfile
    elif _type == "delete_message":
        return Deletmessage
    elif _type == "edit_message":
        return Editmessage
