from pydantic import BaseModel
class AgentCardIn(BaseModel):
    name: str
    description: str
    prompt: str
    image: str
class AgentCardFormat(BaseModel):
    name:str
    description:str
    category:int
    tags:list[str]
    prompt:str
    temperature:float