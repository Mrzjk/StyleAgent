# api/models/agent_card.py
from enum import Enum
from tortoise import fields, models
class StatusEnum(str, Enum):
    draft = "draft"
    active = "active"
    disabled = "disabled"

class VisibilityEnum(str, Enum):
    public = "public"
    private = "private"
    team = "team"
class AgentCard(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField(null=True)
    prompt = fields.TextField()
    image = fields.CharField(max_length=255, null=True)
    
    # 外键使用字符串 "models.ModelName"，related_name 对应 Category/Tag 的反向关联
    category = fields.ForeignKeyField(
        "models.Category", related_name="agents", null=True
    )
    tag = fields.ForeignKeyField(
        "models.Tag", related_name="agents", null=True
    )
    
    version = fields.CharField(max_length=20, default="1.0")
    status = fields.CharEnumField(enum_type=StatusEnum, default=StatusEnum.active)
    visibility = fields.CharEnumField(enum_type=VisibilityEnum, default=VisibilityEnum.public)
    example_inputs = fields.JSONField(null=True)
    example_outputs = fields.JSONField(null=True)
    default_temperature = fields.DecimalField(max_digits=3, decimal_places=2, default=0.70)
    max_tokens = fields.IntField(default=2048)
    tool_bindings = fields.JSONField(null=True)
    author_id = fields.BigIntField(null=True)
    usage_count = fields.IntField(default=0)
    rating = fields.DecimalField(max_digits=2, decimal_places=1, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "t_agent_cards"
