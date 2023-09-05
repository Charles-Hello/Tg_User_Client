# 第一阶段，用于下载tg_user
FROM ubuntu as downloader

# 安装curl、wget和jq工具
RUN apt-get update && apt-get install -y curl wget jq

# 设置工作目录为/app
WORKDIR /app

# 获取最新版本号
RUN LATEST_VAULT_RELEASE=$(curl -s https://api.github.com/repos/Charles-Hello/Tg_User_Client/tags | jq --raw-output '.[0].name') ; wget -O tg_user https://github.com/Charles-Hello/Tg_User_Client/releases/download/${LATEST_VAULT_RELEASE}/linux_tg_user

# 设置文件可执行权限
RUN chmod +x tg_user

# 第二阶段，构建最终镜像
FROM ubuntu

# 设置工作目录为/app
WORKDIR /app

# 复制下载好的tg_user文件
COPY --from=downloader /app/tg_user /app/tg_user

# 复制默认的.env文件到容器内
COPY .env /app/

# 暴露项目所需的端口
EXPOSE 8100 18535

# 设置编码
ENV PYTHONIOENCODING=utf-8

# 启动项目的命令
CMD ["./tg_user"]
