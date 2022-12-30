from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    image = models.ImageField()


    def __str__(self) -> str:
        return self.username 