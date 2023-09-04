# 开始
此文档将引导你使用本项目。
## 许可证
本项目采用 [AGPLv3](https://github.com/Charles-Hello/Tg_User_Client/blob/main/LICENSE) 许可证
::: danger AGPLv3
本项目不带有主动添加，涉及金钱接口，不鼓励、不支持一切商业使用。
:::
## 上游依赖
本项目依赖上游：[Telethon](https://github.com/LonamiWebs/Telethon)。
::: tip Telethon
Telethon是一个asyncio Python 3 MTProto库，用于与Telegram的API进行交互。 作为用户或通过机器人帐户
:::



## Onebot12
本项目使用 [Onebot12](https://12.onebot.dev/) 作为协议进行传输数据
::: tip Onebot12
OneBot 是一个聊天机器人应用接口标准，旨在统一不同聊天平台上的机器人应用开发接口，使开发者只需编写一次业务逻辑代码即可应用到多种机器人平台。
:::
目前支持的通信方式:
 - [x] HTTP
 - [X] HTTP Webhook
 - [x] 正向 WebSocket
 - [x] 反向 WebSocket

## 配置
本项目下的 `.env` 文件为项目配置文件，下面讲解配置文件项目。



# 项目其他的配置项

### `tgusername`
Tgusername 存储凭证
- **类型:** `str`

用于存储 Tgusername 的凭证，方便以后迁移。

### `tg_api_id`
Tg API ID
- **类型:** `int`

Telegram API 的身份标识符。

### `tg_api_hash`
Tg API Hash
- **类型:** `str`

Telegram API 的身份验证哈希值。

### `tg_proxy`
启用 Telegram 代理
- **类型:** `bool`

是否启用 Telegram 代理。

### `tg_proxy_mode`
Telegram 代理模式
- **类型:** `str`

指定 Telegram 代理的模式，例如 'socks5'。

### `tg_proxy_host`
Telegram 代理主机
- **类型:** `str`

Telegram 代理的主机地址。

### `tg_proxy_port`
Telegram 代理端口
- **类型:** `int`

Telegram 代理的端口号。

### `tg_proxy_user`
Telegram 代理用户名
- **类型:** `str`

如果代理需要身份验证，指定代理用户名。

### `tg_proxy_pass`
Telegram 代理密码
- **类型:** `str`

如果代理需要身份验证，指定代理密码。

### `tg_qrlogin`
启用 Tg QR 登录
- **类型:** `bool`

是否启用 Telegram QR 登录功能。

### `tg_qrlogin_qrWeb_port`
Tg QR Web 端口
- **类型:** `int`

启用 QR 登录时的 QR 码 Web 服务端口。

### `tg_qq_email_status`
Tg QQ 邮件状态
- **类型:** `bool`

指定 Tg QQ 登录的邮件状态。

### `tg_qrlogin_qqemail`
Tg QQ 登录邮件
- **类型:** `str`

Tg QQ 登录的邮件地址。

### `tg_qrlogin_qqemail_fakeStr`
qr_emailfake_str 防伪标识符
- **类型:** `str`

Tg QQ 登录邮件的防伪标识符。

# 应用端配置

以下是应用端配置，通常无需更改。

### `application_ws_host`
应用端的 WebSocket 主机
- **类型:** `str`

应用端的 WebSocket 主机地址。

### `application_ws_port`
应用端的 WebSocket 端口
- **类型:** `str`

应用端的 WebSocket 端口号。





### `host`
服务Host
 - **类型:** `IPvAnyAddress`
 - **默认值:** `127.0.0.1`

在使用 `http` 和 `正向 websocket` 方式时会监听此host

### `port`
服务端口
 - **类型:** `int`(1~65535)
 - **默认值:** `8000`

在使用 `http` 和 `正向 websocket` 方式时会监听此端口，注意不要和其他端口冲突！

### `access_token`
访问令牌
 - **类型:** `str`
 - **默认值:** `""`

配置了访问令牌后，与本服务通信的另一端也要配置同样的token，否则会连接失败。

### `heartbeat_enabled`
心跳事件
 - **类型:** `bool`
 - **默认值:** `false`

开启心跳后，将周期向连接端发送心跳事件。

### `heartbeat_interval`
心跳间隔
 - **类型:** `int`(1~65535)
 - **默认值:** `5000`

开启心跳后有用，单位毫秒，必须大于0

### `enable_http_api`
开启http访问
 - **类型:** `bool`
 - **默认值:** `true`

是否开启http访问功能。

### `event_enabled`
启用get_latest_events
 - **类型:** `bool`
 - **默认值:** `false`

开启http时有效，是否启用 `get_latest_events` 原动作

### `event_buffer_size`
缓冲区大小
 - **类型:** `int`
 - **默认值:** `0`

`get_latest_events` 存储的事件缓冲区大小，超过该大小将会丢弃最旧的事件，0 表示不限大小

### `enable_http_webhook`
启用http webhook
 - **类型:** `bool`
 - **默认值:** `false`

是否启用http webhook。

### `webhook_url`
上报地址
 - **类型:** `Set(URL)`
 - **默认值:** `["http://127.0.0.1:8080/onebot/v12/http/"]`

启用webhook生效，webhook 上报地址，需要以`http://`开头，多个地址用`,`分隔。

### `webhook_timeout`
上报请求超时时间
 - **类型:** `int`
 - **默认值:** `5000`

启用webhook生效，单位：毫秒，0 表示不超时

### `websocekt_type`
websocket连接方式
 - **类型:** `str`
 - **默认值:** `Unable`

只能是以下值：
 - `Unable` : 不开启websocket连接
 - `Forward` : 正向websocket连接
 - `Backward` : 反向websocket连接

### `websocket_url`
连接地址
 - **类型:** `Set(URL)`
 - **默认值:** `["ws://127.0.0.1:8080/onebot/v12/ws/"]`

反向websocket连接时生效，反向 WebSocket 连接地址，需要以`ws://`或`wss://`开头，多个地址用`,`分隔。

### `reconnect_interval`
重连间隔
 - **类型:** `int`
 - **默认值:** `5000`

反向websocket连接时生效，反向 WebSocket 重连间隔，单位：毫秒，必须大于 0

### `websocket_buffer_size`
缓冲区大小
 - **类型** `int`
 - **默认值** `4`

反向websocket连接时生效，反向 WebSocket 缓冲区大小，单位：mb，必须大于 0

### `log_level`
日志等级
 - **类型:** `str`
 - **默认值:** `INFO`

一般为以下值：
 - `INFO` : 正常使用
 - `DEBUG` : debug下使用

### `log_days`
保存天数
 - **类型:** `int`
 - **默认值:** `10`

日志保存天数。

### `cache_days`
缓存天数
 - **类型:** `int`
 - **默认值:** `0`

临时文件缓存天数，为0则不清理缓存

## 使用 Nonebot2
本项目支持与 [Nonebot2](https://v2.nonebot.dev/) 进行通信，使用时请注意：
 1. 建议使用反向websocket通信；
 2. nonebot2需要安装onebot适配器，并使用12版本；
