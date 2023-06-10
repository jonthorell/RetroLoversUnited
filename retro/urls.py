from unicodedata import category
from django.urls import path
from .views import Index, Links,Contact, About, Category

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('links', Links.as_view(), name='links'),
    path('contact',Contact.as_view(), name='contact'),
    path('about', About.as_view(), name='about'),
    path('category', Category.as_view(), name='Category')
    ]