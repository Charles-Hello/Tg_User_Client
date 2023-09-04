"""
与TG通信底层


调用消息:
tgchat -> telethon ->msgreporter

上报消息:
msgreporter -> tgchat -> http/ws
"""

from .com_tgchat import tguserApi as tguserApi
from .com_tgchat import MessageReporter as MessageReporter
from .message import MessageHandler as MessageHandler
from .model import Message as Message
