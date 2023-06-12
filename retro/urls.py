from unicodedata import category
from django.urls import path
from .views import Index, Links,Contact, About, Category, Create_article, Test

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('links', Links.as_view(), name='links'),
    path('contact',Contact.as_view(), name='contact'),
    path('about', About.as_view(), name='about'),
    path('category', Category.as_view(), name='Category'),
    path('create_article', Create_article.as_view(), name='Create_article'),
    path('test', Test.as_view(), name='test')
    ]