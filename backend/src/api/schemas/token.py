from pydantic import BaseModel,Field,EmailStr
from typing import Annotated
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    id:int
    username:Annotated[str,Field(min_length=3,max_length=20,description="注册的用户名")]
   
class FormData(BaseModel):
    username:Annotated[str,Field(min_length=3,max_length=20,description="注册的用户名")]
    password:Annotated[str,Field(min_length=3,max_length=20,description="注册的密码")]