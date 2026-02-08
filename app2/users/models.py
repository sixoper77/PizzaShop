from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to="users_image", blank=True, null=True)
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username
