from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Model


class AuthToken(Model):
    key = models.CharField(max_length=255, null=False, blank=False)
    create_at = models.DateTimeField(null=False, blank=False)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
