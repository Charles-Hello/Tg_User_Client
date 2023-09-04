# 消息段
本项目目前实现了部分标准消息段及拓展消息段
:::tip onebot12
`消息段:` 表示聊天消息的一个部分，在一些平台上，聊天消息支持图文混排，其中就会有多个消息段，分别表示每个图片和每段文字。
:::

## 纯文本<Badge text="标准" type="success" />
type: `text`

表示一段纯文本。
 - [x] 可以接收
 - [x] 可以发送

::: tabs
@tab 参数
| 字段名    | 数据类型 | 说明       |
| :-------: | :------: | :--------: |
| `text`    | string   | 纯文本内容 |

@tab 示例
```json
{
    "type": "text",
    "data": {
        "text": "这是一个纯文本"
    }
}
```

@tab nb2使用
``` python
from nonebot.adapters.onebot.v12 import MessageSegment

message = MessageSegment.text("这是一个纯文本")
```
:::



## 图片<Badge text="标准" type="success" />
type:`image`

表示一张图片。

- [x] 可以接收
- [x] 可以发送

::: tabs

@tab 参数

|  字段名   | 数据类型 |    说明     |
| :-------: | :------: | :---------: |
| `file_id` |  string  | 图片文件 ID |

@tab 示例

```json
{
    "type": "image",
    "data": {
        "file_id": "e30f9684-3d54-4f65-b2da-db291a477f16"
    }
}
```

@tab nb2使用
```python
from nonebot.adapters.onebot.v12 import MessageSegment

message = MessageSegment.image(file_id="e30f9684-3d54-4f65-b2da-db291a477f16")
```

:::

## 语音<Badge text="标准" type="success" />
type: `voice`


::: warning 未实现

本应用未实现此字段

:::


## 音频<Badge text="标准" type="success" />
type: `audio`

音频文件。

::: warning 未实现

本应用未实现此字段

:::

## 视频<Badge text="标准" type="success" />
type: `video`

视频消息

- [x] 可以接收
- [ ] 可以发送

:::tabs

@tab 参数

|  字段名   | 数据类型 |    说明     |
| :-------: | :------: | :---------: |
| `file_id` |  string  | 视频文件 ID |

@tab 示例

```json
{
    "type": "video",
    "data": {
        "file_id": "e30f9684-3d54-4f65-b2da-db291a477f16"
    }
}
```



:::

## 文件<Badge text="标准" type="success" />
type: `file`

文件消息

- [x] 可以接收
- [x] 可以发送

:::tabs

@tab 参数

|  字段名   | 数据类型 |    说明     |
| :-------: | :------: | :---------: |
| `file_id` |  string  |     文件 ID |

@tab 示例

```json
{
    "type": "file",
    "data": {
        "file_id": "e30f9684-3d54-4f65-b2da-db291a477f16"
    }
}
```

@tab nb2使用
```python
from nonebot.adapters.onebot.v12 import MessageSegment

message = MessageSegment.file(file_id="e30f9684-3d54-4f65-b2da-db291a477f16")
```

:::




## 回复<Badge text="标准" type="success" />
type: `reply`

回复消息。

::: warning 未实现

本应用未实现此字段

:::



