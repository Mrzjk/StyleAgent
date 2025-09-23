from pydantic import BaseModel
class AgentIn(BaseModel):
    name: str
    description: str
    prompt: str
