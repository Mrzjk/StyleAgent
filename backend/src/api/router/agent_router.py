
import logging
from fastapi.routing import APIRouter
from fastapi import Depends
from api.models import AgentCard,Tag,Category,AgentTag
from api.schemas import AgentCardIn,ResponseModel,AgentIn,AgentCardFormat
from api.utils import get_current_user
agent_router = APIRouter(prefix="/agent",dependencies=[Depends(get_current_user)])
logger = logging.getLogger(__name__)
@agent_router.get("/")
async def all_agents():
    """获取所有智能体"""
    agent_cards = await AgentCard.all().prefetch_related("category").values(
    "id", "name", "description", "prompt", "image",
    category_id="category__id",
    style_name="category__name",
    )
    # logging.info(f"获取所有智能体中{agent_cards}")
    
    for agent_card in agent_cards:
        agent_id = agent_card['id']
        agent_card["tags"]=[]
        logging.info(f"依次遍历智能体中{agent_card}")
        tags = await AgentTag.filter(agent_id=agent_id).values("tag_id")
        for tag in tags:
            tag_id = tag["tag_id"]
            tag_name = await Tag.filter(id=tag_id).first().values("name")
            logging.info(f"当前智能体的获取标签中{tag_name}")
            agent_card["tags"].append( tag_name['name'])
    
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
async def create_agent(agent_card: AgentCardFormat):
    """创建智能体"""
    # 创建 AgentCard
    logging.info(f"创建智能体中..........")
    agent = await AgentCard.create(
        name=agent_card.name,
        description=agent_card.description,
        prompt=agent_card.prompt,
        temperature=agent_card.temperature,
        category_id=agent_card.category
    )
    logging.info(f"创建智能体成功，id为{agent.id}")
   
    # 1.获取智能体目前所有的标签，避免重复
    agent_tags = await AgentTag.filter(agent_id = agent.id).values("id","tag_id","agent_id")
    logging.info(f"获取智能体目前所有的标签，避免重复，结果为{agent_tags}")
    # 2.获取智能体所有标签的name
    agent_names = []
    for data in agent_tags:
        tag_id = data['tag_id']
        tag_name = Tag.filter(id=tag_id).first().values("name")
        agent_names.append(tag_name)
    logging.info(f"获取智能体所有标签的name，结果为{agent_names}")
    logging.info(f"目前创建智能体的标签为{agent_card.tags}")
    #3.判断添加的标签，是否已经存在，如果不存在，则先创建标签，然后将记录智能体和标签的id
    for name in agent_card.tags:
        if name not in agent_names:
            # 判断这个标签是否存在，不存在，则创建
            search_tag = await Tag.filter(name=name).first()
            logging.info(f"判断这个标签是否存在，结果为{search_tag}, 类型={type(search_tag)}")
            logging.info(f"{search_tag is None}")
            if search_tag is None:
                logging.info(f"{name}不存在，则创建标签")
                search_tag = await Tag.create(name=name)
                logging.info(f"{search_tag.name}不存在，则创建标签成功，id为{search_tag.id}")
            logging.info(f"目前的标签：{search_tag},类型：{type(search_tag)}")
            await AgentTag.create(tag_id=search_tag.id,agent_id =agent.id)
    logging.info(f"添加标签成功")
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


@agent_router.post("/optimize_system_prompt/")
async def optimize_system_prompt(agent_info:AgentIn):
    """优化系统提示"""
    agent_name,agent_description,agent_style = agent_info.model_dump().values()
    return ResponseModel(
        data=agent_info,
        message="优化系统提示成功"
    )