from django.db import models

class User(models.Model):
    name = models.CharField()
    email = models.EmailField()
    password = models.CharField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name}-{self.email}"
