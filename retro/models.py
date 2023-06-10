# from getpass import getuser
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User=get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False)
    def __str__ (self):
        return self.name

class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=60, blank=False, null=False)
    content = models.TextField(max_length=2000, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Links(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    url = models.CharField(max_length=255, blank=False, null=False)
    alt = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name
