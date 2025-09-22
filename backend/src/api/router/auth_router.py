import os
from tortoise.exceptions import IntegrityError
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import timedelta

from api.models import User
from api.utils import get_password_hash, verify_password
from api.utils import create_access_token
from api.schemas import ResponseModel,UserIn
from api.schemas import Token, TokenData

auth_router = APIRouter(prefix="auth")
@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    user = await User.filter(username=username).first().values("id","username","password_hash","email")
    if user is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    password_hash = user['password_hash']
    if not await verify_password(form_data.password, password_hash):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    minutes = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES'))
    access_token_expires = timedelta(minutes=minutes)*60*24
    sub = TokenData(username=user['username'],email=user['email'])
    access_token = await create_access_token(data=sub.model_dump(), expires_delta=access_token_expires)
    content = ResponseModel(
        code=status.HTTP_200_OK,
        msg="Login success",
        data={
            "username": user['username'],
            "email": user['email'],
            "expires_in": minutes * 60
        }
    ).model_dump()
    response  = JSONResponse(content=content)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Strict",
        secure=True
    )
    return response

@auth_router.post("/register")
async def register(user: UserIn):
    user_data = user.model_dump()
    user_data["password_hash"] = await get_password_hash(user_data.pop("password"))

    # 检查用户名和邮箱
    existing_user = await User.filter(username=user.username).first()
    if existing_user:
        return ResponseModel(code=400, msg="用户名已存在")
    existing_email = await User.filter(email=user.email).first()
    if existing_email:
        return ResponseModel(code=400, msg="邮箱已存在")

    # 创建用户
    try:
        user_obj = await User.create(**user_data)
    except IntegrityError:
        return ResponseModel(code=400, msg="用户名或邮箱已存在")

    return ResponseModel(data=user.model_dump(), msg="注册成功")