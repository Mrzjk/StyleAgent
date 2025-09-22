from tortoise import fields, models
from enum import Enum

# 枚举定义
class AgentCardStatus(str, Enum):
    draft = 'draft'
    active = 'active'
    disabled = 'disabled'

class Visibility(str, Enum):
    public = 'public'
    private = 'private'
    team = 'team'

# AgentCard 模型
class AgentCard(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField(null=True)
    prompt = fields.TextField()
    image = fields.CharField(max_length=255, null=True)
    category = fields.CharField(max_length=50, null=True)
    tags = fields.JSONField(null=True)
    version = fields.CharField(max_length=20, default='1.0')
    
    # 使用枚举
    status = fields.CharEnumField(enum_type=AgentCardStatus, default=AgentCardStatus.active)
    visibility = fields.CharEnumField(enum_type=Visibility, default=Visibility.public)
    
    example_inputs = fields.JSONField(null=True)
    example_outputs = fields.JSONField(null=True)
    default_temperature = fields.DecimalField(max_digits=3, decimal_places=2, default=0.7)
    max_tokens = fields.IntField(default=2048)
    tool_bindings = fields.JSONField(null=True)
    author_id = fields.BigIntField(null=True)
    usage_count = fields.IntField(default=0)
    rating = fields.DecimalField(max_digits=2, decimal_places=1, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "t_agent_cards"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.version})"
