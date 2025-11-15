from django.db import models
from django.urls import reverse

class User(models.Model):
    name = models.CharField()
    email = models.EmailField()
    password = models.CharField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name}-{self.email}"
    
    # def get_absolute_url(self):
    #     return reverse("user_detail", kwargs={"pk": self.pk})
    
