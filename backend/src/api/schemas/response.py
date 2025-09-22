from pydantic import BaseModel
from typing import Any, List, Optional
from starlette import status
class ResponseModel(BaseModel):
    code: int = status.HTTP_200_OK           # 状态码
    msg: str = "success"      # 消息
    data: Optional[Any] = None  # 数据
