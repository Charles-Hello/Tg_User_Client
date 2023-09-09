import json
from tgbot_client.com_tgchat.type import WxType
from pathlib import Path
from tgbot_client.consts import FILE_CACHE
from uuid import uuid4
    
    
    
async def event_handel(event,bot):
    class_sender = await event.get_sender()
    reply = await event.get_reply_message()
    if reply:
        reply_message = reply.message
        reply_sender_id =reply.sender_id
    else:
        reply_message =""
        reply_sender_id =""
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
        "reply_message":reply_message,
        "reply_sender_id":reply_sender_id
    }
    return json.dumps(msg_dict)