# 常见报错
此文档将告诉你场景的报错类型以及解决方案。
:::tip telethon上游端
1. Server closed the connection: 0 bytes read on a total of 8 expected bytes  <br>上游依赖连接检验(可以忽略，不影响使用) <br><br>
2. telethon.network.mtprotosender: Attempt 1 at connecting failed: TimeoutError  <br>上游依赖连接检验 (可以忽略，不影响使用)<br><br>
3. The api_id/api_hash combination is invalid (caused by SendCodeRequest)  <br>表示你配置文件里面的tg_api_id和tg_api_hash填写不正确，请前往https://my.telegram.org/auth获取你的api和hash<br><br>
4. Attempt 1 at connecting failed: ConnectionError: [Errno 111] Could not connect to proxy 192.168.1.36:9050 [Connect call failed ('192.168.1.36', 9050)]  <br>代理错误<br><br>
5. Security error while unpacking a received message: Server replied with a wrong session ID <br>您使用的代理可能会以某种方式干扰。
正在或已经在其他地方使用电视马拉松会话。 确保您从电视马拉松创建了会话，并且没有使用 在其他任何地方都相同会话。如果您需要使用来自 多个地方，登录并为您需要的每个地方使用不同的会话。一般为网络错误导致的<br><br>
:::


