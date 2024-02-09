from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Trials(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add=True)
    