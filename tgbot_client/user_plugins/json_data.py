import json
import os
from pathlib import Path
from tgbot_client.consts import DOWNLOAD_TIMEOUT, FILE_CACHE,ASP_WORK
from toollib.guid import SnowFlake
snow = SnowFlake()

cwd = Path(".") / ASP_WORK
# 定时任务存储的 JSON 文件路径
TASKS_FILE_PATH = Path(".") / ASP_WORK / 'tasks.json'

def add_task(name, sender, text, cron_expression,status):
    """
    添加定时任务，将任务信息存储到 JSON 文件中。
    """
    tasks = load_tasks()
    new_task = {
        'id': str(snow.gen_uid()),
        'name': name,
        'sender': sender,
        'text': text,
        'cron_expression': cron_expression,
        'status':status
    }
    tasks.append(new_task)
    save_tasks(tasks)

def list_tasks():
    """
    查询全部定时任务，返回任务列表。
    """
    tasks = load_tasks()
    content = ""
    if len(tasks) > 0:
        for task in tasks:
            if task['status']:
                open_status =f'✅\n提示如需暂停：`暂停定时{task["id"]}`'
            else:
                open_status =f'❌\n提示如需恢复：`恢复定时{task["id"]}`'
            content +=(f"Task ID: `{task['id']}`\nName: {task['name']}\n👻发送chatID: {task['sender']}\n🌟发送内容: {task['text']}\n🎃时间表达式: {task['cron_expression']}\n😮定时状态: {open_status}\n修改定时内容：`修改定时{task['id']}@我是超人#10秒`\n删除定时：`删除定时{task['id']}`\n\n-------------\n\n")
        # content += f"❗️`删除全部定时`"
    else:
        content="你当前无定时任务！✏️\n请使用`定时(发送的文本)@(时间表达式)`进行新增！"
    return content

def delete_task(task_id):
    """
    删除指定 ID 的定时任务，更新 JSON 文件，并返回删除的任务信息。
    """
    tasks = load_tasks()
    deleted_task_info = ""

    for task in tasks:
        if task['id'] == task_id:
            deleted_task_info+=f"删除的id信息\nid：{task['id']}\n聊天id：{task['sender']}\n内容：{task['text']}"
            tasks.remove(task)
            break

    save_tasks(tasks)
    if deleted_task_info =="":
        deleted_task_info = f"✨没有这个{task_id}定时任务哦亲！！\n别搞错了！"
    return deleted_task_info


def delete_all_tasks():
    """
    删除全部定时任务，清空 JSON 文件，并返回删除的任务信息列表。
    """
    save_tasks([]) 



def modify_task(task_id, new_text=None, new_cron_expression=None,status=None):
    """
    修改指定 ID 的定时任务，更新 JSON 文件。
    """
    tasks = load_tasks()
    Content  =""
    for task in tasks:
        if task['id'] == task_id:
            Content+=f"❣️当前修改的id为：{task_id}\n"
            if new_text !="":
                task['text'] = new_text
                Content+=f"💖修改后的内容为：{new_text}\n"
            if new_cron_expression !="":
                task['cron_expression'] = new_cron_expression
                Content+=f"💝修改后的时间表达式为：{new_cron_expression}\n"
            if status:
                task['status'] = status
                Content+=f"💝修改后的开关为：{status}\n"
            break
    save_tasks(tasks)
    if Content =="":
          Content = f"✨没有这个{task_id}定时任务哦亲！！\n别修改错了！"
    return Content

def load_tasks():
    """
    从 JSON 文件中加载定时任务。
    """
    if not os.path.exists(TASKS_FILE_PATH):
        return []
    try:
        with open(TASKS_FILE_PATH, 'r', encoding="utf-8") as file:
            tasks = json.load(file)
    except json.JSONDecodeError:
        tasks = []
    return tasks

def save_tasks(tasks):
    """
    将定时任务保存到 JSON 文件中。
    """
    with open(TASKS_FILE_PATH, 'w', encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)


# # 示例使用：
# # # 添加定时任务
# # add_task("Task 1", "User1", "Hello, World!", "*/20 * * * *")

# # 查询全部定时任务
# # list_tasks()

# # # 删除定时任务
# delete_task(3)

# # 修改定时任务
# # modify_task(4, new_cron_expression="1212121211")

# # 查询修改后的全部定时任务
# list_tasks()
