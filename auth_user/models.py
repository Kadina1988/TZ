from django.db import models
from django.urls import reverse

import secrets

class Role(models.Model):
    name = models.CharField(unique=True)
    
    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=20, unique=True)
    password = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, default=3)
    
    def __str__(self):
        return f"{self.name}-{self.email}"
    

class AccessToken(models.Model):
    token = models.CharField()
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.token = secrets.token_hex(16)
        super().save(*args, **kwargs)
    
