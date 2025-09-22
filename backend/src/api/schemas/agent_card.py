from pydantic import BaseModel
class AgentCardIn(BaseModel):
    name: str
    description: str
    prompt: str
    image: str