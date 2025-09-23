# api/models/category.py
from tortoise import fields, models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .agent_card import AgentCard

class Category(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=True)
    description = fields.CharField(max_length=255, null=True)
    create_time = fields.DatetimeField(null=True)
    update_time = fields.DatetimeField(null=True)

    # 反向关联，类型提示用
    agents: fields.ReverseRelation["AgentCard"]

    class Meta:
        table = "t_category"
