# 消息动作


## 发送消息<Badge text="标准" type="success" />
action: `send_message`

:::warning Tgchat
由于 tgchat 的特性，该接口有以下限制:
 - `message_type` 只能为 `private` 或 `group`
 - `message` 中的每个消息段都将作为一条消息发送出去(除了`mention`)
 - `mention` 和 `mention_all` 只支持群聊
:::

:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `message_type` | string | 消息类型，`private` 或 `group` |
| `user_id` | string | 用户 ID，当 `detail_type` 为 `private` 时必须传入 |
| `group_id` | string | 群 ID，当 `detail_type` 为 `group` 时必须传入 |
| `message` | message | 消息内容，为消息段列表，详见 [消息段](/message/README.md) |

@tab 响应数据
在 `Onebot12` 标准中，原则上应该返回一个 `message_id`，但是由于hook的限制，目前只能返回一个 `bool`，用来判断消息是否发送成功。

@tab 请求示例
```json
{
    "action": "send_message",
    "params": {
        "detail_type": "group",
        "group_id": "12467",
        "message": [
            {
                "type": "text",
                "data": {
                    "text": "我是文字巴拉巴拉巴拉"
                }
            }
        ]
    }
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": true,
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    message = MessageSegment.text("我是文字巴拉巴拉巴拉") +
              MessageSegment.image(file_id="asd-asd-asd-ads")
    await bot.send_message(detail_type="group",group_id="12467",message=message)

```

:::

## 撤回消息<Badge text="标准" type="success" />
action: `delete_message`


:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `message` | string | 要删除的信息|
| `chat_id` | string | 聊天的id |


@tab 响应数据
无。

@tab 请求示例
```json
{
    "action": "delete_message",
    "params": {
        "chat_id": "12121211",
        "message":"string"
    }
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": true,
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    await bot.delete_message(chat_id=event.user_id,message=message)

```

:::




## 编辑消息<Badge text="标准" type="success" />
action: `edit_message`


:::tabs

@tab 请求参数
| 字段名    | 数据类型 |    说明    |
| :-------: | :------: | :--------: |
| `before_message` | string | 要编辑的信息|
| `after_message` | string | 编辑信息的内容|
| `chat_id` | string | 聊天的id |


@tab 响应数据
无。

@tab 请求示例
```json
{
    "action": "edit_message",
    "params": {
        "before_message":"string",
        "after_message":"string",
        "chat_id": "12121211",

    }
}
```

@tab 响应示例
```json
{
    "status": "ok",
    "retcode": 0,
    "data": true,
    "message": ""
}
```

@tab 在nb2使用
```python
from nonebot.adapters.onebot.v12 import Bot, MessageSegment
from nonebot import get_bot

async def test():
    bot = get_bot()
    await bot.edit_message(chat_id=event.user_id,before_message=before_message,after_message=after_message)

```

:::
