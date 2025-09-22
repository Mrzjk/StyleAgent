from tortoise import fields, models

class User(models.Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True, null=True)
    phone = fields.CharField(max_length=20, unique=True, null=True)
    password_hash = fields.CharField(max_length=255)
    salt = fields.CharField(max_length=50, null=True)
    status = fields.IntField(default=1)  # 0=禁用, 1=启用, 2=封禁
    role = fields.CharField(max_length=20, default='user')
    last_login_at = fields.DatetimeField(null=True)
    last_login_ip = fields.CharField(max_length=45, null=True)
    profile = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)  # 软删除

    class Meta:
        table = "users"
        indexes = [
            ("email",),
            ("phone",),
            ("status",)
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return self.username
