import os 

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from api.schemas import UserIn
from api.schemas import ResponseModel
from api.utils import get_password_hash,verify_password
from api.utils import get_current_user
from api.models import User
user_router = APIRouter(prefix="/user",dependencies=[Depends(get_current_user)])
@user_router.get("/")
async def all_users():
    data = await User.all().values("id","username","email")
    return ResponseModel(
        data=data,
        msg="获取用户信息成功"
)
@user_router.get("/{user_id}")
async def get_user(user_id:int):
    """获取单个用户信息"""
    data = await User.filter(id=user_id).values("id","username","email")
    return ResponseModel(
        data=data,
        msg="获取用户信息成功"
    )
@user_router.post("/")
async def create_user(user:UserIn):
    """创建用户"""
    user_data = user.model_dump()
    user_data["password_hash"] =await get_password_hash(user_data["password"])
    user_data.pop("password")
    user = await User.create(**user_data)
    return ResponseModel(
        data=user,
        msg="创建用户成功"
    )
@user_router.put("/{user_id}")
async def update_user(user_id:int ,user:UserIn):
    
    """更新用户信息"""
    user_data = user.model_dump()
    user_data["password_hash"] =await get_password_hash(user_data["password"])
    user_data.pop("password")
    user = await User.update(**user_data).where(User.id==user_id).gino.first()
    return ResponseModel()
@user_router.delete("/{user_id}")
async def delete_user(user_id:int):
    """删除用户"""
    deleted_count = await User.delete().where(User.id==user_id).gino.first()
    return ResponseModel(
        data=deleted_count,
        msg="删除用户成功"
    )
    