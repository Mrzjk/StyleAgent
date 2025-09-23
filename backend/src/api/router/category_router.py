from fastapi.routing import APIRouter
from fastapi import Depends
from api.models import Category
from api.schemas import CategoryIn, ResponseModel
from api.utils import get_current_user

category_router = APIRouter(prefix="/category", dependencies=[Depends(get_current_user)])


@category_router.get("/", response_model=ResponseModel)
async def all_categories() -> ResponseModel:
    """获取所有分类"""
    categories = await Category.all().values("id", "name", "description")
    return ResponseModel(data=categories, msg="success")


@category_router.post("/", response_model=ResponseModel)
async def create_category(category: CategoryIn) -> ResponseModel:
    """创建分类"""
    try:
        new_category = await Category.create(**category.model_dump())
        return ResponseModel(data=new_category, msg="success")
    except Exception as e:
        return ResponseModel(data=None, code=400, msg=str(e))


@category_router.put("/{category_id}", response_model=ResponseModel)
async def update_category(category_id: int, category: CategoryIn) -> ResponseModel:
    """更新分类"""
    try:
        updated_count = await Category.filter(id=category_id).update(**category.model_dump())
        if updated_count:
            updated_category = await Category.get(id=category_id).values("id", "name", "description")
            return ResponseModel(data=updated_category, msg="success")
        return ResponseModel(data=None, code=404, msg="Category not found")
    except Exception as e:
        return ResponseModel(data=None, code=400, msg=str(e))


@category_router.delete("/{category_id}", response_model=ResponseModel)
async def delete_category(category_id: int) -> ResponseModel:
    """删除分类"""
    try:
        deleted_count = await Category.filter(id=category_id).delete()
        if deleted_count:
            return ResponseModel(data=None, msg="success")
        return ResponseModel(data=None, code=404, msg="Category not found")
    except Exception as e:
        return ResponseModel(data=None, code=400, msg=str(e))
