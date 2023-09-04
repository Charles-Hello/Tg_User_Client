"""
TG客户端抽象，整合各种请求需求:
 - 处理`driver`: 上下发送请求
 - 处理`com_tgchat`: 维护与tguser的连接
 - 处理`api`: 处理api调用
"""
from .tgchat import TgChatManager as TgChatManager
