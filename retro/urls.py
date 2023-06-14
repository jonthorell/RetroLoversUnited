
from django.urls import path
from .views import Index, Links,Contact, About, Category, Create_article, Test, Login, Logout, Create_account, Thankyou

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('links', Links.as_view(), name='links'),
    path('contact',Contact.as_view(), name='contact'),
    path('about', About.as_view(), name='about'),
    path('category', Category.as_view(), name='Category'),
    path('create_article', Create_article.as_view(), name='Create_article'),
    path('test', Test.as_view(), name='test'),
    path('login', Login.as_view(), name='Login'),
    path('logout', Logout.as_view(), name='Logout'),
    path('create_account', Create_account.as_view(), name='create_account'),
    path('thankyou', Thankyou.as_view(), name='thankyou')
    ]