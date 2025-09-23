from enum import Enum
from tortoise import fields, models
class AgentTag(models.Model):
    id = fields.IntField(pk=True, generated=True)
    agent = fields.ForeignKeyField("models.AgentCard", related_name="agent_tags")
    tag = fields.ForeignKeyField("models.Tag", related_name="tag_agents")
    class Meta:
        table = "t_agent_tag"