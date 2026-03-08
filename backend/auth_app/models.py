from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    failed_login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    lock_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    blocked_until = models.DateTimeField()

    def __str__(self):
        return self.ip_address