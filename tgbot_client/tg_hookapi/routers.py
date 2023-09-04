from fastapi import APIRouter
from tgbot_client.tg_hookapi import function

router = APIRouter()

# 自定义总路由，实现业务分发

router.include_router(function.router, tags=["TgUser-Api"])
