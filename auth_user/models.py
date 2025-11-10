from django.db import models
from django.contrib.auth.models import User 

class User(models.Model):
    name = models.CharField()
    email = models.EmailField()
    password = models.CharField()
    is_active = models.BooleanField(default=True)
