from tgbot_client.action_manager.bot_core import bot
from telethon import events, TelegramClient, functions
import asyncio
from apscheduler.triggers.cron import CronTrigger
from telethon.tl.types import ChannelForbidden
import re
from .apscheduler_config import content as apscheduler_config
from .json_data import add_task, list_tasks, delete_task, modify_task,delete_all_tasks
from .aspscheduler_init import Scheduler_data,init_scheduled_tasks

@bot.client.on(events.NewMessage(pattern=r"^id$", outgoing=True))
@bot.client.on(events.MessageEdited(pattern=r"^id$", outgoing=True))
async def id(event):
    """
    查询您回复的消息的发件人的 UserID且设置定时发送文本
    """
    message = await event.get_reply_message()
    text = "Message ID: `" + str(event.message.id) + "`\n\n"
    text += "**Chat**\nChat_id:" + str(event.chat_id) + "\n"
    msg_from = event.chat if event.chat else (await event.get_chat())
    if event.is_private:
        try:
            text += "first_name: `" + msg_from.first_name + "`\n"
        except TypeError:
            text += "**死号**\n"
        if msg_from.last_name:
            text += "last_name: `" + msg_from.last_name + "`\n"
        if msg_from.username:
            text += "username: @" + msg_from.username + "\n"
        if msg_from.lang_code:
            text += "lang_code: `" + msg_from.lang_code + "`\n"
    if event.is_group or event.is_channel:
        text += "title: `" + msg_from.title + "`\n"  # 需要
        try:
            if msg_from.username:
                text += "username: @" + msg_from.username + "\n"
        except AttributeError:
            await event.edit("出错了呜呜呜 ~ 当前聊天似乎不是群聊。")
            return
        text += "date: `" + str(msg_from.date) + "`\n"
    if message:
        text += (
            "\n"
            + "以下是被回复消息的信息"
            + "\nMessage ID: `"
            + str(message.id)
            + "`\n\n**User**\nid: `"
            + str(message.sender_id)
            + "`"
        )
        try:
            if message.sender.bot:
                text += f"\nis_bot: 是"
            try:
                text += "\nfirst_name: `" + message.sender.first_name + "`"
            except TypeError:
                text += f"\n**死号**"
            if message.sender.last_name:
                text += "\nlast_name: `" + message.sender.last_name + "`"
            if message.sender.username:
                text += "\nusername: @" + message.sender.username
            if message.sender.lang_code:
                text += "\nlang_code: `" + message.sender.lang_code + "`"
        except AttributeError:
            pass
        if message.forward:
            if str(message.forward.chat_id).startswith("-100"):
                text += (
                    "\n\n**Forward From Channel**\nid: `"
                    + str(message.forward.chat_id)
                    + "`\ntitle: `"
                    + message.forward.chat.title
                    + "`"
                )
                if not isinstance(message.forward.chat, ChannelForbidden):
                    if message.forward.chat.username:
                        text += "\nusername: @" + message.forward.chat.username
                    text += "\nmessage_id: `" + str(message.forward.channel_post) + "`"
                    if message.forward.post_author:
                        text += "\npost_author: `" + message.forward.post_author + "`"
                    text += "\ndate: `" + str(message.forward.date) + "`"
            else:
                if message.forward.sender:
                    text += (
                        "\n\n**Forward From User**\nid: `"
                        + str(message.forward.sender_id)
                        + "`"
                    )
                    try:
                        if message.forward.sender.bot:
                            text += f"\nis_bot: 是"
                        try:
                            text += (
                                "\nfirst_name: `"
                                + message.forward.sender.first_name
                                + "`"
                            )
                        except TypeError:
                            text += f"\n**死号**"
                        if message.forward.sender.last_name:
                            text += (
                                "\nlast_name: `"
                                + message.forward.sender.last_name
                                + "`"
                            )
                        if message.forward.sender.username:
                            text += "\nusername: @" + message.forward.sender.username
                        if message.forward.sender.lang_code:
                            text += (
                                "\nlang_code: `"
                                + message.forward.sender.lang_code
                                + "`"
                            )
                    except AttributeError:
                        pass
                    text += "\ndate: `" + str(message.forward.date) + "`"
    msg = await event.edit(text)

#---------------------------我是业务代码分割线------------------------

@bot.client.on(events.NewMessage(from_users=bot.client._self_id, pattern=r"^u$|^U$"))
async def user(event):
    msg = await event.respond("我叫喵酱~💕")
    await asyncio.sleep(2)
    await msg.delete()












@bot.client.on(events.NewMessage(pattern=r"^查询定时$|^定时查询$", outgoing=True))
async def check(event):
    content = list_tasks()

    await event.edit(content)


@bot.client.on(events.NewMessage(pattern=r"^删除定时(.*)", outgoing=True))
async def delete(event):
    Apsmessages = event.raw_text

    delete_number = re.findall(r"删除定时(.*)", Apsmessages)[0]
    deleted_task_info = delete_task(delete_number)

    await event.edit("🖤删除的定时任务状态\n" + deleted_task_info)
    Scheduler_data.apscheduler_data.shutdown()
    init_scheduled_tasks()
    
@bot.client.on(events.NewMessage(pattern=r"^删除全部定时$", outgoing=True))
async def delete(event):


    delete_all_tasks()

    await event.edit("❤️‍🩹已经为你删除全部定时任务！")
    msg = await event.respond("你当前无定时任务！✏️\n请使用`定时(发送的文本)@(时间表达式)`进行新增！")
    Scheduler_data.apscheduler_data.shutdown()
    init_scheduled_tasks()
    


@bot.client.on(events.NewMessage(pattern=r"^修改定时(.*)@.*#.*", outgoing=True))
async def edit(event):
    Apsmessages = event.raw_text
    modify_Content = re.findall(r"@(.*)#", Apsmessages)[0]
    modify_cron = re.findall(r"#(.*)", Apsmessages)[0]
    delete_number = re.findall(r"修改定时(.*)@", Apsmessages)[0]
    modify_Content = modify_task(task_id=delete_number,new_text=modify_Content, new_cron_expression=modify_cron)

    await event.edit("😍修改的定时任务信息\n" + modify_Content)
    Scheduler_data.apscheduler_data.shutdown()
    init_scheduled_tasks()


@bot.client.on(events.NewMessage(pattern=r"^定时指令$", outgoing=True))
async def get(event):
    msg = await event.respond(apscheduler_config)