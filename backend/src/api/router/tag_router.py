from fastapi.routing import APIRouter
from fastapi import Depends
from api.models import Tag
from api.schemas import TagIn, ResponseModel
from api.utils import get_current_user

tag_router = APIRouter(
    prefix="/tag",
    dependencies=[Depends(get_current_user)]
)


@tag_router.get("/", response_model=ResponseModel)
async def all_tags() -> ResponseModel:
    """获取所有标签"""
    try:
        tags = await Tag.all().values("id", "name", "create_time", "update_time")
        return ResponseModel(data=tags, msg="success")
    except Exception as e:
        return ResponseModel(data=None, code=400, msg=str(e))


@tag_router.get("/{tag_id}", response_model=ResponseModel)
async def get_tag(tag_id: int) -> ResponseModel:
    """获取单个标签"""
    try:
        tag = await Tag.filter(id=tag_id).values("id", "name", "create_time", "update_time").first()
        if not tag:
            return ResponseModel(data=None, code=404, msg="Tag not found")
        return ResponseModel(data=tag, msg="success")
    except Exception as e:
        return ResponseModel(data=None, code=400, msg=str(e))


@tag_router.post("/", response_model=ResponseModel)
async def create_tag(tag: TagIn) -> ResponseModel:
    """创建标签"""
    try:
        new_tag = await Tag.create(**tag.model_dump())
        return ResponseModel(data=new_tag, msg="标签创建成功")
    except Exception as e:
        return ResponseModel(data=None, code=400, msg=str(e))


@tag_router.put("/{tag_id}", response_model=ResponseModel)
async def update_tag(tag_id: int, tag: TagIn) -> ResponseModel:
    """更新标签"""
    try:
        updated_count = await Tag.filter(id=tag_id).update(**tag.model_dump())
        if updated_count:
            updated_tag = await Tag.get(id=tag_id).values("id", "name", "create_time", "update_time")
            return ResponseModel(data=updated_tag, msg="标签更新成功")
        return ResponseModel(data=None, code=404, msg="Tag not found")
    except Exception as e:
        return ResponseModel(data=None, code=400, msg=str(e))


@tag_router.delete("/{tag_id}", response_model=ResponseModel)
async def delete_tag(tag_id: int) -> ResponseModel:
    """删除标签"""
    try:
        deleted_count = await Tag.filter(id=tag_id).delete()
        if deleted_count:
            return ResponseModel(data=None, msg="标签删除成功")
        return ResponseModel(data=None, code=404, msg="Tag not found")
    except Exception as e:
        return ResponseModel(data=None, code=400, msg=str(e))
