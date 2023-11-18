import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime
from telethon import events, TelegramClient, functions
import asyncio
from tgbot_client.action_manager.bot_core import bot
from apscheduler.triggers.cron import CronTrigger
from telethon.tl.types import ChannelForbidden
import os
import re
from pathlib import Path
from tgbot_client.consts import ASP_WORK
from .send_http import send_text
from .json_data import add_task, list_tasks, delete_task, modify_task, delete_all_tasks


class Apscheduler_data:
    apscheduler_data = BackgroundScheduler(timezone="Asia/Shanghai")


def get_all_task_ids(Scheduler_data):
    """
    获取所有定时任务的任务ID。
    """
    job_ids = [job.id for job in Scheduler_data.apscheduler_data.get_jobs()]
    return job_ids


# 定时任务存储的 JSON 文件路径
TASKS_FILE_PATH = Path(".") / ASP_WORK / "tasks.json"


def init_scheduled_tasks():
    """
    初始化定时任务，从 JSON 文件中读取任务信息并创建对应的定时任务。
    """
    if not os.path.exists(TASKS_FILE_PATH):
        print("请创建你的定时任务，因为 JSON 文件不存在。")
        return

    tasks = load_tasks()
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    Scheduler_data.apscheduler_data = scheduler
    for task in tasks:
        if task.get("status", False):  # Check if status is True
            try:
                if "秒" in task.get("cron_expression"):
                    seconds = re.findall(r"\d+", task.get("cron_expression"))[0]
                    scheduler.add_job(
                        run_task,
                        "interval",
                        seconds=int(seconds),
                        args=[(task["sender"], task["text"])],
                        id=str(task["id"]),
                        timezone="Asia/Shanghai",
                        next_run_time=datetime.datetime.now().astimezone(),
                    )
                    print(
                        f"Success in task {task['id']}: {task['name']} - {task['sender']} - {task['text']} - 设置表达式成功"
                    )
                else:
                    trigger = CronTrigger.from_crontab(task["cron_expression"])
                    scheduler.add_job(
                        run_task,
                        trigger=trigger,
                        args=[(task["sender"], task["text"])],
                        id=str(task["id"]),
                        timezone="Asia/Shanghai",
                        next_run_time=datetime.datetime.now().astimezone(),
                    )
                    print(
                        f"Success in task {task['id']}: {task['name']} - {task['sender']} - {task['text']} - 设置表达式成功"
                    )
            except ValueError:
                print(
                    f"Error in task {task['id']}: {task['name']} - Invalid cron expression: {task['cron_expression']}"
                )
                continue
        else:
            print(f"Skipping task {task['id']}: {task['name']} - 定时状态为false，不执行")

    scheduler.start()


def run_task(action):
    """
    执行定时任务的动作。
    """
    sender, text = action
    print("发送者:", sender)
    print("文本:", text)
    send_text(text, sender)


def load_tasks():
    try:
        with open(TASKS_FILE_PATH, encoding="utf-8") as file:
            tasks = json.load(file)
    except UnicodeDecodeError as e:
        print(f"Error decoding JSON file: {e}")
        tasks = []

    return tasks


def pause_task(apscheduler_data, task_id):
    """
    暂停指定任务并更新 JSON 文件。
    """
    status = False
    content = ""
    tasks = load_tasks()
    for task in tasks:
        if task.get("id") == task_id:
            task["status"] = False  # Update status to False
            status = True
            content += f"任务id：{task_id}成功暂停！"
            break
    if status:
        apscheduler_data.pause_job(str(task_id))
        save_tasks(tasks)
    else:
        content += f"没有该任务id：{task_id}\n❗️再仔细检查id后再操作暂停定时任务"
    return content


def resume_task(apscheduler_data, task_id):
    """
    恢复指定任务并更新 JSON 文件。
    """
    status = False
    content = ""
    tasks = load_tasks()
    for task in tasks:
        if task.get("id") == task_id:
            task["status"] = True  # Update status to True
            status = True
            content += f"任务id：{task_id}成功恢复！"
            break
    if status:
        try:
            save_tasks(tasks)
            apscheduler_data.resume_job(str(task_id))
        except:
            apscheduler_data.shutdown()
            init_scheduled_tasks()
    else:
        content += f"没有该任务id：{task_id}\n❗️再仔细检查id后再操作恢复定时任务"
    return content


def save_tasks(tasks):
    """
    将定时任务保存到 JSON 文件中。
    """
    with open(TASKS_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)


@bot.client.on(events.NewMessage(pattern=r"^恢复定时(.*)", outgoing=True))
async def _(event):
    Apsmessages = event.raw_text
    delete_number = re.findall(r"恢复定时(.*)", Apsmessages)[0]
    resume_Content = resume_task(Scheduler_data.apscheduler_data, delete_number)

    await event.edit("😍恢复定时任务信息\n" + resume_Content)


@bot.client.on(events.NewMessage(pattern=r"^暂停定时(.*)", outgoing=True))
async def _(event):
    Apsmessages = event.raw_text
    delete_number = re.findall(r"暂停定时(.*)", Apsmessages)[0]
    pause_Content = pause_task(Scheduler_data.apscheduler_data, delete_number)

    await event.edit("🥵暂停定时任务信息\n" + pause_Content)


@bot.client.on(events.NewMessage(pattern=r"^定时.*@.*", outgoing=True))
@bot.client.on(events.MessageEdited(pattern=r"^定时.*@.*", outgoing=True))
async def add(event):
    """
    查询您回复的消息的发件人的 UserID且设置定时发送文本
    """
    Apsmessages = event.raw_text
    # */20 * * * *
    # 从这里写拿到转发文本和cron设置，还得匹配cron正确不正确。不正确的话，则edit提醒，三秒后删除
    #
    #
    ApsSend_Text = re.findall(r"定时(.*)@", Apsmessages)[0]
    cron_expression = re.findall(r"@(.*)", Apsmessages)[0]
    if "秒" not in cron_expression:
        try:
            trigger = CronTrigger.from_crontab(cron_expression)
        except ValueError:
            msg = await event.edit("这个时间表达式不正确\n请重新设置！")
            await asyncio.sleep(2)
            await msg.delete()
            return

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
    chatid = re.findall(r"Chat_id:(.*)", text)[0]
    add_task("定时发送文本", chatid, ApsSend_Text, cron_expression, True)
    msg_text = (
        f"❤️新增定时发送信息：\n聊天id：{chatid}\n文本内容：{ApsSend_Text}\n时间表达式：{cron_expression}\n"
    )
    msg = await event.edit(msg_text)
    await asyncio.sleep(4)
    await msg.delete()
    Scheduler_data.apscheduler_data.shutdown()
    init_scheduled_tasks()


Scheduler_data = Apscheduler_data()
# 示例使用：
# 初始化定时任务
# init_scheduled_tasks()
# 示例使用：
# 获取所有定时任务的任务ID并打印
# all_task_ids = get_all_task_ids(apscheduler_data)
# print("所有定时任务的任务ID:", all_task_ids)
# 暂停任务（示例）
# pause_task(apscheduler_data,"1725541142419734528")

# # 恢复任务（示例）
# resume_task(apscheduler_data,"1725541142419734528")

# # 运行 scheduler 任务
# while True:
#     time.sleep(1)
