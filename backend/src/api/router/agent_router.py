
from fastapi.routing import APIRouter
from fastapi import Depends
from api.models import AgentCard
from api.schemas import AgentCardIn
from api.schemas import ResponseModel
from api.utils import get_current_user
agent_router = APIRouter(prefix="/agent",dependencies=[Depends(get_current_user)])

@agent_router.get("/")
async def all_agents():
    """获取所有智能体"""
    agent_cards =  await AgentCard.all().values("id","name","description","prompt","image")
    return ResponseModel(
        data=agent_cards,
        message="获取所有智能体成功"
    )
@agent_router.get("/{agent_id}")
async def get_agent(agent_id:int):
    """获取单个智能体"""
    agent_card =  await AgentCard.filter(id=agent_id).values("id","name","description","prompt","image")
    return ResponseModel(
        data=agent_card,
        message="获取单个智能体成功"
    )
@agent_router.post("/")
async def create_agent(agent_card:AgentCardIn):
    """创建智能体"""
    agent_card = await AgentCard.create(**agent_card.dict())
    return ResponseModel(
        data=agent_card,
        message="创建智能体成功"
    )
@agent_router.put("/{agent_id}")
async def update_agent(agent_id:int,agent_card:AgentCardIn):
    """更新智能体"""
    agent_card = await AgentCard.filter(id=agent_id).update(**agent_card.dict())
    return ResponseModel(
        data=agent_card,
        message="更新智能体成功"
    )
@agent_router.delete("/{agent_id}")
async def delete_agent(agent_id:int):
    """删除智能体"""
    agent_card = await AgentCard.filter(id=agent_id).delete()
    return ResponseModel(
        data=agent_card,
        message="删除智能体成功"
    )
