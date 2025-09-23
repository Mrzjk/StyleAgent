from pydantic import BaseModel,Field
from typing import Any, List, Optional,Annotated
from starlette import status
from datetime import datetime
class CategoryIn(BaseModel):
    name: Annotated[str,Field(min_length=3,max_length=20,description="大模型的风格")]
    description: str
    create_time: Optional[datetime]
    update_time: Optional[datetime]
