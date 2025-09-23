from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TagIn(BaseModel):
    name: str
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None