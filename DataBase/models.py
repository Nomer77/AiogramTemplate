from tortoise.models import Model
from tortoise import fields

class TelegramUsers(Model):
    TelegramID = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.TelegramID)
