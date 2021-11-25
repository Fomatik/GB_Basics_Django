from datetime import datetime, timedelta
from django.conf import settings
import pytz
from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='возраст')

    activate_key = models.CharField(max_length=128, blank=True, null=True, verbose_name='Ключ активации')
    activate_key_expired = models.DateTimeField(blank=True, null=True)

    def is_activate_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.activate_key_expired + timedelta(hours=48):
            return True
        return False

    def activate_user(self):
        user.is_active = True
        user.activate_key = None
        user.activate_key_expired = None
        user.save()