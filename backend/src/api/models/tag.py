# api/models/tag.py
from tortoise import fields, models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .agent_card import AgentCard

class Tag(models.Model):
    id = fields.IntField(pk=True, generated=True)
    name = fields.CharField(max_length=255, null=True)
    create_time = fields.DatetimeField()
    update_time = fields.DatetimeField(null=True)


    class Meta:
        table = "t_tag"
