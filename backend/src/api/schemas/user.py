from pydantic import BaseModel,EmailStr,Field
from typing import Annotated
class UserIn(BaseModel):
    id:Annotated[int,Field(description="用户id")]
    username:Annotated[str,Field(min_length=3,max_length=20,description="注册的用户名")]
    password:Annotated[str,Field(min_length=3,max_length=20,description="注册的用户的密码")]
    email:Annotated[EmailStr,Field(description="注册的邮箱")]


class UserOut(BaseModel):
    pass