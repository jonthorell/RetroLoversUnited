# from getpass import getuser

from collections import UserString
from django.db.models import CharField, Model
from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from django.urls import reverse
from autoslug import AutoSlugField

# Create your models here.

# status is used to check wheter comment or article has been approved. Some of this has been adapted for my own use from the codestar code-along
# Articles have their status automatically set to published (although can be changed). If not changed, it is immediately visible. 
# User needs to be a member of the editors group to be able to create an article and the only one that can do that
# is the superuser, so presumably those that can create articles have been deemed trustworthy.

# Comments are in draft status by default. That means an admin has to approve the comment before it can be seen



STATUS = ((0, "Draft"), (1,"Published"))
RATING = ((0, "Not rated"), (1,"Really Low"), (2,"Low"), (3,"Medium"), (4,"Good"), (5,"Excellent"))

User=get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.CharField(max_length=200, blank=False, null=False)
    avatar = models.CharField(max_length=60, blank=False, null=False, default="default-category.png")

    class Meta:
        ordering = ['name']

    def __str__ (self):
        return self.name

    def get_absolute_url(self):
        return reverse("articles_by_category", args=[str(self.id)])

class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)
    slug = AutoSlugField(populate_from='title', unique=True)
    title = models.CharField(max_length=60, blank=False, null=False, unique=True)
    content = models.TextField(max_length=2000, blank=False, null=False)
    updated_on = models.DateTimeField(auto_now=True)
    featured_image = CloudinaryField('image', default='placeholder')
    created_on = models.DateTimeField(auto_now_add=True)
    excerpt = models.TextField(blank=False, null=False)
    status = models.IntegerField(choices=STATUS, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ratings = models.ManyToManyField(
        User, related_name='article_rating', blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return (
            f"Title: {self.title[:30]}..., "
            f"Editor: {self.user} "
            f"({self.created_on:%Y-%m-%d %H:%M}): "
        )

    def get_absolute_url(self):
        return reverse("article_detail", args=[str(self.id)])

    def number_of_ratings(self):
        return self.ratings.count()

class Link(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    url = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.CharField(max_length=255, blank=False, null=False)
    alt = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name



class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user')
    body = models.TextField(max_length=200,blank=False, null=False)
    slug = AutoSlugField(populate_from='name', unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return (
            f"User: {self.name}, "
            f"body: {self.body[:30]}..., "
            f"({self.created_on:%Y-%m-%d %H:%M}): "
        )

class Profile(models.Model):
    short_description = models.CharField(max_length=60, blank=False, null=False)
    description = models.TextField(max_length=2000, blank=False, null=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    computer = models.TextField(max_length=400, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=60, default="default-user.png")
    slug = AutoSlugField(populate_from='short_description', unique=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.short_description

    def get_absolute_url(self):
        return reverse("view_profile", args=[str(self.id)])

