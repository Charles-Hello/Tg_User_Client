import{_ as p}from"./plugin-vue_export-helper-c27b6911.js";import{r as o,o as t,c,a as s,b as a,d as e,e as n}from"./app-6a854ac3.js";const i="/Tg_User_Client/assets/image-557562a9.png",r={},b=n(`<h2 id="设置配置" tabindex="-1"><a class="header-anchor" href="#设置配置" aria-hidden="true">#</a> 设置配置</h2><h3 id="参考调整" tabindex="-1"><a class="header-anchor" href="#参考调整" aria-hidden="true">#</a> 参考调整</h3><div class="hint-container tip"><p class="hint-container-title">config</p><p>项目目录下的.env文件是本项目的配置文件，创建参考并设置：</p></div><div class="language-text" data-ext="text"><pre class="shiki" style="background-color:#282c34;"><code><span class="line"><span style="color:#abb2bf;"># #################################################</span></span>
<span class="line"><span style="color:#abb2bf;"># tg的配置项                  #</span></span>
<span class="line"><span style="color:#abb2bf;"># 如需使用socks5代理则对应安装即可</span></span>
<span class="line"><span style="color:#abb2bf;"># For Python &gt;= 3.6 : install python-socks[asyncio]</span></span>
<span class="line"><span style="color:#abb2bf;"># For Python &lt;= 3.5 : install PySocks</span></span>
<span class="line"><span style="color:#abb2bf;"># ################################################</span></span>
<span class="line"><span style="color:#abb2bf;">tgusername=&quot;session_name&quot;</span></span>
<span class="line"><span style="color:#abb2bf;"># 存储Tgusername的凭证，方便以后迁移</span></span>
<span class="line"><span style="color:#abb2bf;">tg_api_id=111111</span></span>
<span class="line"><span style="color:#abb2bf;">tg_api_hash=&quot;11111111111111111111111111111111111&quot;</span></span>
<span class="line"><span style="color:#abb2bf;">tg_proxy=True</span></span>
<span class="line"><span style="color:#abb2bf;">tg_proxy_mode=&#39;socks5&#39;</span></span>
<span class="line"><span style="color:#abb2bf;">tg_proxy_host=&#39;192.168.1.36&#39;</span></span>
<span class="line"><span style="color:#abb2bf;">tg_proxy_port=9050</span></span>
<span class="line"><span style="color:#abb2bf;">tg_proxy_user=&#39;&#39;</span></span>
<span class="line"><span style="color:#abb2bf;">tg_proxy_pass=&#39;&#39;</span></span>
<span class="line"><span style="color:#abb2bf;">tg_qrlogin=false</span></span>
<span class="line"><span style="color:#abb2bf;">tg_qrlogin_qrWeb_port=18535</span></span>
<span class="line"><span style="color:#abb2bf;">tg_qq_email_status = True</span></span>
<span class="line"><span style="color:#abb2bf;">#接收登录二维码qq邮箱</span></span>
<span class="line"><span style="color:#abb2bf;">tg_qrlogin_qqemail=&#39;1xxxxxxxx@qq.com&#39;</span></span>
<span class="line"><span style="color:#abb2bf;"># qr_emailfake_str 防伪标识符</span></span>
<span class="line"><span style="color:#abb2bf;">tg_qrlogin_qqemail_fakeStr=&#39;你好呀！赛利亚！&#39;</span></span>
<span class="line"><span style="color:#abb2bf;"># #################################################</span></span>
<span class="line"><span style="color:#abb2bf;"># 应用端(一般勿动)                  #</span></span>
<span class="line"><span style="color:#abb2bf;"># ################################################</span></span>
<span class="line"><span style="color:#abb2bf;"></span></span>
<span class="line"><span style="color:#abb2bf;">application_ws_host=&quot;127.0.0.1&quot;</span></span>
<span class="line"><span style="color:#abb2bf;">&quot;&quot;&quot;应用端的ws的host主机&quot;&quot;&quot;</span></span>
<span class="line"><span style="color:#abb2bf;">application_ws_port=&quot;18000&quot;</span></span>
<span class="line"><span style="color:#abb2bf;">&quot;&quot;&quot;应用端的ws的port端口&quot;&quot;&quot;</span></span>
<span class="line"><span style="color:#abb2bf;"></span></span>
<span class="line"><span style="color:#abb2bf;"># #################################################</span></span>
<span class="line"><span style="color:#abb2bf;"># onebot12的配置项                  #</span></span>
<span class="line"><span style="color:#abb2bf;"># ################################################</span></span>
<span class="line"><span style="color:#abb2bf;"></span></span>
<span class="line"><span style="color:#abb2bf;"># 服务host</span></span>
<span class="line"><span style="color:#abb2bf;">host=127.0.0.1</span></span>
<span class="line"><span style="color:#abb2bf;"># 服务端口</span></span>
<span class="line"><span style="color:#abb2bf;">port=8100</span></span>
<span class="line"><span style="color:#abb2bf;"># 访问令牌</span></span>
<span class="line"><span style="color:#abb2bf;">access_token=&quot;&quot;</span></span>
<span class="line"><span style="color:#abb2bf;"># 心跳事件</span></span>
<span class="line"><span style="color:#abb2bf;">heartbeat_enabled=false</span></span>
<span class="line"><span style="color:#abb2bf;"># 心跳间隔(毫秒)</span></span>
<span class="line"><span style="color:#abb2bf;">heartbeat_interval=5000</span></span>
<span class="line"><span style="color:#abb2bf;"></span></span>
<span class="line"><span style="color:#abb2bf;"># HTTP 通信</span></span>
<span class="line"><span style="color:#abb2bf;"># 是否开启http api</span></span>
<span class="line"><span style="color:#abb2bf;">enable_http_api=true</span></span>
<span class="line"><span style="color:#abb2bf;"># 是否启用 get_latest_events 元动作，启用http api时生效</span></span>
<span class="line"><span style="color:#abb2bf;">event_enabled=true</span></span>
<span class="line"><span style="color:#abb2bf;"># 事件缓冲区大小，超过该大小将会丢弃最旧的事件，0 表示不限大小</span></span>
<span class="line"><span style="color:#abb2bf;">event_buffer_size=0</span></span>
<span class="line"><span style="color:#abb2bf;"></span></span>
<span class="line"><span style="color:#abb2bf;"># HTTP Webhook</span></span>
<span class="line"><span style="color:#abb2bf;"># 是否启用http webhook</span></span>
<span class="line"><span style="color:#abb2bf;">enable_http_webhook=false</span></span>
<span class="line"><span style="color:#abb2bf;"># webhook 上报地址，启用webhook生效</span></span>
<span class="line"><span style="color:#abb2bf;">webhook_url=[&quot;http://127.0.0.1:8080/onebot/v12/http/&quot;]</span></span>
<span class="line"><span style="color:#abb2bf;"># 上报请求超时时间，单位：毫秒，0 表示不超时</span></span>
<span class="line"><span style="color:#abb2bf;">webhook_timeout=5000</span></span>
<span class="line"><span style="color:#abb2bf;"></span></span>
<span class="line"><span style="color:#abb2bf;"># websocket连接方式，只能是以下值</span></span>
<span class="line"><span style="color:#abb2bf;"># - Unable      不开启websocket连接</span></span>
<span class="line"><span style="color:#abb2bf;"># - Forward     正向websocket连接</span></span>
<span class="line"><span style="color:#abb2bf;"># - Backward    反向websocket连接</span></span>
<span class="line"><span style="color:#abb2bf;">websocekt_type=&quot;Backward&quot;</span></span>
<span class="line"><span style="color:#abb2bf;"># 反向 WebSocket 连接地址，使用反向websocket时生效</span></span>
<span class="line"><span style="color:#abb2bf;">websocket_url=[&quot;ws://127.0.0.1:8080/onebot/v12/ws/&quot;]</span></span>
<span class="line"><span style="color:#abb2bf;"># 反向 WebSocket 重连间隔，单位：毫秒，必须大于 0</span></span>
<span class="line"><span style="color:#abb2bf;">reconnect_interval=5000</span></span>
<span class="line"><span style="color:#abb2bf;"># 反向 WebSocket 的缓冲区大小，单位(Mb)</span></span>
<span class="line"><span style="color:#abb2bf;">websocket_buffer_size=4</span></span>
<span class="line"><span style="color:#abb2bf;"># #################################################</span></span>
<span class="line"><span style="color:#abb2bf;"># 项目其他的配置项                  #</span></span>
<span class="line"><span style="color:#abb2bf;"># ################################################</span></span>
<span class="line"><span style="color:#abb2bf;"></span></span>
<span class="line"><span style="color:#abb2bf;"># 日志显示等级</span></span>
<span class="line"><span style="color:#abb2bf;">log_level=&quot;INFO&quot;</span></span>
<span class="line"><span style="color:#abb2bf;"># 日志保存天数</span></span>
<span class="line"><span style="color:#abb2bf;">log_days=10</span></span>
<span class="line"><span style="color:#abb2bf;"># 文件缓存天数，为0则不清理缓存，每天凌晨清理</span></span>
<span class="line"><span style="color:#abb2bf;">cache_days=3</span></span>
<span class="line"><span style="color:#abb2bf;"></span></span></code></pre></div><h2 id="可执行文件运行" tabindex="-1"><a class="header-anchor" href="#可执行文件运行" aria-hidden="true">#</a> 可执行文件运行</h2><div class="hint-container tip"><p class="hint-container-title">提示</p><p>Github找到Releases寻找你对应的平台进行下载</p><h3 id="window" tabindex="-1"><a class="header-anchor" href="#window" aria-hidden="true">#</a> Window</h3><p>创建.env配置文件，参考配置，与可执行文件放在一起，然后运行window_tg_user.exe</p><h3 id="linux" tabindex="-1"><a class="header-anchor" href="#linux" aria-hidden="true">#</a> Linux</h3><div class="language-bash" data-ext="sh"><pre class="shiki" style="background-color:#282c34;"><code><span class="line"><span style="color:#ABB2BF;">chmod +x linux_tg_user</span></span>
<span class="line"><span style="color:#ABB2BF;">./linux_tg_user</span></span>
<span class="line"></span></code></pre></div><p>创建.env配置文件，参考配置，与可执行文件放在一起。参考上述代码</p><h3 id="macos" tabindex="-1"><a class="header-anchor" href="#macos" aria-hidden="true">#</a> Macos</h3><div class="language-bash" data-ext="sh"><pre class="shiki" style="background-color:#282c34;"><code><span class="line"><span style="color:#ABB2BF;">chmod a+x macos_tg_user</span></span>
<span class="line"><span style="color:#ABB2BF;">./macos_tg_user</span></span>
<span class="line"></span></code></pre></div><p>创建.env配置文件，参考配置，与可执行文件放在一起。参考上述代码 Macos可能会出现阻止使用,因为来自不明身份证开发者等等字段 <img src="`+i+'" alt="Macos image"> 打开设置-&gt;隐私与安全性-&gt;安全性-&gt;点击仍然允许</p></div><h2 id="使用windows或linux开发部署" tabindex="-1"><a class="header-anchor" href="#使用windows或linux开发部署" aria-hidden="true">#</a> 使用windows或linux开发部署</h2><h3 id="python环境" tabindex="-1"><a class="header-anchor" href="#python环境" aria-hidden="true">#</a> python环境</h3>',8),d={class:"hint-container tip"},h=s("p",{class:"hint-container-title"},"python",-1),y={href:"https://www.python.org/",target:"_blank",rel:"noopener noreferrer"},f=n(`<h3 id="虚拟环境" tabindex="-1"><a class="header-anchor" href="#虚拟环境" aria-hidden="true">#</a> 虚拟环境</h3><p>强烈推荐使用虚拟环境运行bot，使用何种虚拟环境由你指定，这里列出比较常用的：</p><div class="hint-container tip"><p class="hint-container-title">venv</p><p>venv是python自带的虚拟环境工具，linux下可能需要手动安装：</p><div class="language-bash" data-ext="sh"><pre class="shiki" style="background-color:#282c34;"><code><span class="line"><span style="color:#7F848E;font-style:italic;"># 需要先安装venv模块</span></span>
<span class="line"><span style="color:#ABB2BF;">sudo apt-get install python3.10-venv</span></span>
<span class="line"><span style="color:#7F848E;font-style:italic;"># 创建虚拟环境</span></span>
<span class="line"><span style="color:#ABB2BF;">python -m venv ./venv</span></span>
<span class="line"></span>
<span class="line"><span style="color:#7F848E;font-style:italic;"># 激活虚拟环境</span></span>
<span class="line"><span style="color:#56B6C2;">source</span><span style="color:#ABB2BF;"> ./venv/bin/activate</span></span>
<span class="line"></span></code></pre></div><p>windows下可以直接使用：</p><div class="language-bash" data-ext="sh"><pre class="shiki" style="background-color:#282c34;"><code><span class="line"><span style="color:#7F848E;font-style:italic;"># windows下，创建venv目录</span></span>
<span class="line"><span style="color:#ABB2BF;">python -m venv ./venv</span></span>
<span class="line"></span>
<span class="line"><span style="color:#7F848E;font-style:italic;"># 激活虚拟环境</span></span>
<span class="line"><span style="color:#ABB2BF;">./venv/scripts/activate</span></span>
<span class="line"></span></code></pre></div></div><div class="hint-container tip"><p class="hint-container-title">conda</p><p>使用conda管理环境，甚至包括python的环境也能管理：</p><div class="language-bash" data-ext="sh"><pre class="shiki" style="background-color:#282c34;"><code><span class="line"><span style="color:#7F848E;font-style:italic;"># 创建环境</span></span>
<span class="line"><span style="color:#ABB2BF;">conda create --name bot python=3.10</span></span>
<span class="line"></span>
<span class="line"><span style="color:#7F848E;font-style:italic;"># 激活环境</span></span>
<span class="line"><span style="color:#ABB2BF;">conda activate bot</span></span>
<span class="line"></span></code></pre></div></div><h3 id="安装依赖" tabindex="-1"><a class="header-anchor" href="#安装依赖" aria-hidden="true">#</a> 安装依赖</h3><p>环境准备好后需要安装依赖，同样有几种方式：</p><div class="hint-container tip"><p class="hint-container-title">pip安装</p><p>在激活虚拟环境后，进入bot目录，使用pip安装依赖：</p><div class="language-bash" data-ext="sh"><pre class="shiki" style="background-color:#282c34;"><code><span class="line"><span style="color:#ABB2BF;">pip install -r requirements.txt</span></span>
<span class="line"></span></code></pre></div></div><div class="hint-container tip"><p class="hint-container-title">conda安装</p><p>使用conda可以在虚拟环境外安装依赖，在bot目录下：</p><div class="language-bash" data-ext="sh"><pre class="shiki" style="background-color:#282c34;"><code><span class="line"><span style="color:#ABB2BF;">conda install --yes --file requirements.txt</span></span>
<span class="line"></span></code></pre></div></div><h3 id="运行本项目" tabindex="-1"><a class="header-anchor" href="#运行本项目" aria-hidden="true">#</a> 运行本项目</h3><h4 id="调整配置文件-后运行" tabindex="-1"><a class="header-anchor" href="#调整配置文件-后运行" aria-hidden="true">#</a> 调整配置文件，后运行</h4><div class="hint-container tip"><p class="hint-container-title">运行项目</p><p>在项目目录下：</p><div class="language-bash" data-ext="sh"><pre class="shiki" style="background-color:#282c34;"><code><span class="line"><span style="color:#ABB2BF;">python3 main.py</span></span>
<span class="line"></span></code></pre></div></div><h3 id="后台运行" tabindex="-1"><a class="header-anchor" href="#后台运行" aria-hidden="true">#</a> 后台运行</h3>`,12),u={class:"hint-container tip"},_=s("p",{class:"hint-container-title"},"screen",-1),v={href:"https://www.runoob.com/linux/linux-comm-screen.html",target:"_blank",rel:"noopener noreferrer"},B=n(`<h2 id="使用docker部署" tabindex="-1"><a class="header-anchor" href="#使用docker部署" aria-hidden="true">#</a> 使用Docker部署</h2><h3 id="部署说明" tabindex="-1"><a class="header-anchor" href="#部署说明" aria-hidden="true">#</a> 部署说明</h3><div class="hint-container tip"><p class="hint-container-title">部署前准备</p><p>首先要求你自身要有docker环境，没有的请自行搜索安装</p><div class="language-bash" data-ext="sh"><pre class="shiki" style="background-color:#282c34;"><code><span class="line"><span style="color:#ABB2BF;">mkdir tguser</span></span>
<span class="line"><span style="color:#56B6C2;">cd</span><span style="color:#ABB2BF;"> tguser</span></span>
<span class="line"><span style="color:#7F848E;font-style:italic;">#参考配置文件，按照填写配置</span></span>
<span class="line"><span style="color:#ABB2BF;">vi .env</span></span>
<span class="line"><span style="color:#7F848E;font-style:italic;">#其中的port：8100，18535为默认映射端口，如需更改，请根据你的.env文件配置</span></span>
<span class="line"><span style="color:#7F848E;font-style:italic;">#这里“你的env绝对路径”的C:\\Users\\a1140\\Desktop\\Tg_User_Clinet\\.env是你.env的文件位置</span></span>
<span class="line"><span style="color:#ABB2BF;">docker run -it -p 8100:8100 -p 18535:18535 --name tguser -v 你的env绝对路径:/app/.env 1140601003/tguserclient:latest</span></span>
<span class="line"><span style="color:#7F848E;font-style:italic;">#em:</span></span>
<span class="line"><span style="color:#ABB2BF;">docker run -it -p 8100:8100 -p 18535:18535 --name tguser -v C:</span><span style="color:#E5C07B;">\\U</span><span style="color:#ABB2BF;">sers</span><span style="color:#E5C07B;">\\a</span><span style="color:#ABB2BF;">1140</span><span style="color:#E5C07B;">\\D</span><span style="color:#ABB2BF;">esktop</span><span style="color:#E5C07B;">\\T</span><span style="color:#ABB2BF;">g_User_Clinet</span><span style="color:#E5C07B;">\\.</span><span style="color:#ABB2BF;">env:/app/.env 1140601003/tguserclient:latest</span></span>
<span class="line"></span></code></pre></div><p>启动后按照要求，如需要退出交互式，请按键盘的<code>ctrl+z</code>,再按<code>ctrl+c</code>即可关闭前台输出，这样docker容器后台也正常执行。可以使用<code>docker logs tguser</code>查看后台输出日志，如果有其他的错误请反馈给我！</p></div>`,3);function g(k,x){const l=o("ExternalLinkIcon");return t(),c("div",null,[b,s("div",d,[h,s("p",null,[a("项目采用python环境部署，版本需要在"),s("a",y,[a("python3.10"),e(l)]),a("以上，python怎么安装请自行解决。")])]),f,s("div",u,[_,s("p",null,[a("linux下运行后没法收起到后台？可以自己选择后台运行的工具，我这里使用的是screen："),s("a",v,[a("教程"),e(l)])])]),B])}const m=p(r,[["render",g],["__file","DEPLPY.html.vue"]]);export{m as default};
