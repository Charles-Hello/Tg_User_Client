import importlib

from fastapi import FastAPI

from tgbot_client.config import Config, Env
from tgbot_client.driver import Driver
from tgbot_client.log import default_filter, log_init, logger
from tgbot_client.tgchat import TgChatManager


_TgChat: TgChatManager = None
"""TG管理器"""


async def init() -> None:
    """
    初始化client
    """
    global _TgChat
    env = Env()
    config = Config(_common_config=env.dict())
    default_filter.level = config.log_level
    log_init(config.log_days)
    logger.info(f"Current <y><b>Env: {env.environment}</b></y>")
    logger.debug(f"Loaded <y><b>Config</b></y>: {str(config.dict())}")

    _TgChat = TgChatManager(config)
    # 这里初始化配置文件
    await _TgChat.init()


def run() -> None:
    """
    启动
    """
    driver = get_driver()
    driver.run()


def get_driver() -> Driver:
    """
    获取后端驱动器
    """
    tgchat = get_Tgchat()
    return tgchat.driver


def get_Tgchat() -> TgChatManager:
    """
    获取tgchat管理器
    """
    if _TgChat is None:
        raise ValueError("tgchat管理端尚未初始化...")
    return _TgChat


def get_app() -> FastAPI:
    """获取 Server App 对象。

    返回:
        Server App 对象

    异常:
        ValueError: 全局 `Driver` 对象尚未初始化 (`tgchatferry_client.init` 尚未调用)
    """
    driver = get_driver()
    return driver.server_app


def load(name: str) -> None:
    """
    加载指定的模块
    """
    importlib.import_module(name)
    logger.success(f"<g>加载[{name}]成功...</g>")
