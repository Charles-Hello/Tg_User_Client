from fastapi import APIRouter, Query, Depends, HTTPException, Body
from typing import Optional, Dict, Any
from .model import ApiManger

from pathlib import Path
from base64 import b64decode
from tgbot_client.file_manager import FileCache, FileManager
from typing import Annotated, Union

router = APIRouter()


@router.post(
    "/send_text",
    name="发送文本信息",
    description="""
    传messags[str]和wxid[str]参数
""",
)
async def _(item: ApiManger("send_text")):
    try:
        await item.run()
        return {"status": "ok"}
    except Exception:
        return HTTPException(status_code=400, detail="Failed to send text to WebSocket")


@router.post(
    "/send_photo",
    name="发送图片信息",
    description="""
    传fileid[str]和wxid[str]参数
""",
)
async def _(item: ApiManger("send_file")):
    try:
        await item.run()
        return {"status": "ok"}
    except Exception:
        return HTTPException(status_code=401, detail="Failed to send file to WebSocket")

#TODO 待修，还需要把getfile加上根据id找路径
@router.post(
    "/get_self_info",
    name="获取self的信息",
    description="""
    不用传参数
""",
)
async def _(item: ApiManger("get_self_info")):
    try:
        return await item.run()
    except Exception:
        return HTTPException(
            status_code=402, detail="Failed to send self_info to WebSocket"
        )


@router.post(
    "/get_id_info",
    name="获取id实体的信息",
    description="""
    传实体id[int]
""",
)
async def _(item: ApiManger("get_id_info")):
    try:
        return await item.run()
    except Exception:
        return HTTPException(
            status_code=402, detail="Failed to send self_info to WebSocket"
        )


@router.post(
    "/upload_file",
    response_model=None,
    name="上传文件",
    description="""
    传dict
    "type"：表示上传类型，可以是 "url"、"path" 或 "data"。
    "name"：文件的名称。
    "magic"（仅当 type 为 "url" 时）：文件的 URL 地址。
    "magic"（仅当 type 为 "path" 时）：文件的本地路径。
    "magic"（仅当 type 为 "data" 时）：文件的数据，可以是Base64编码的字符串。
""",
)
async def _(
    params: Annotated[
        ApiManger("upload_file"),
        Body(
            examples=[
                {
                    "type": "url",
                    "name": "banne_photo28.jpg",
                    "magic": "https://xxxxx/banne_photo28.png",
                },
            ],
        ),
    ],
):
    try:
        if params.type == "url":
            if params.magic is None:
                return {
                    "status": "failed",
                    "retcode": 10003,
                    "data": None,
                    "message": "缺少url参数",
                }
            file_id = await FileManager().cache_file_id_from_url(
                params.magic, params.name, None
            )
            if file_id is None:
                return {
                    "status": "failed",
                    "retcode": 33000,
                    "data": None,
                    "message": "下载文件失败",
                }
            return {"status": "ok", "retcode": 0, "data": {"file_id": file_id}}
        if params.type == "path":
            if params["path"] is None:
                return {
                    "status": "failed",
                    "retcode": 10003,
                    "data": None,
                    "message": "缺少path参数",
                }
            file_id = await FileManager().cache_file_id_from_path(
                Path(params["path"]), name=params.name, copy=False
            )
            if file_id is None:
                return {
                    "status": "failed",
                    "retcode": 32000,
                    "data": None,
                    "message": "操作文件失败",
                }
            return {"status": "ok", "retcode": 0, "data": {"file_id": file_id}}
        if params.data is None:
            return {
                "status": "failed",
                "retcode": 10003,
                "data": None,
                "message": "缺少data参数",
            }
        if isinstance(params.data, str):
            params.data = b64decode(params.data)
        file_id = await FileManager().cache_file_id_from_data(params.data, params.name)
        return {"status": "ok", "retcode": 0, "data": {"file_id": file_id}}

    except Exception as e:
        print(e)
        return HTTPException(
            status_code=402, detail="Failed to send self_info to WebSocket"
        )
