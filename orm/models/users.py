from tortoise.models import Model
from tortoise import fields


class TelegramUser(Model):
    TelegramID = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=255, null=True, blank=True)
    is_admin = fields.BooleanField(default=False)
    is_banned = fields.BooleanField(default=False)
