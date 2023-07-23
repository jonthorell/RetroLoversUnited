
from . import views
from django.urls import path
from .views import Index, Links,Contact, About, Kategories, Thankyou, Test, edit_profile, View_profile,List_Users,article_detail,articles_by_category,articles_by_author,create_article,my_Articles,view_my_profile

#app_name = "retro"

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('links', Links.as_view(), name='links'),
    path('links/page/<int:page>',views.listing_links, name='listing-links-by-page'),
    #path('links.json', views.listing_api, name='links-api'),
    path('article.json', views.listing_article_api, name='article-api'),
    path('contact',Contact.as_view(), name='contact'),
    path('about', About.as_view(), name='about'),
    path('category', Kategories.as_view(), name='Kategories'),
    path('create_article', create_article, name='create_article'),
    path('test', Test.as_view(), name='test'),
    path('thankyou', Thankyou.as_view(), name='thankyou'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path("view_profile", View_profile.as_view(), name='view_profile'),
    path("view_my_profile", view_my_profile.as_view(), name='view__my_profile'),
    path('list_users', List_Users.as_view(), name='list_users'),
    path("article/<int:pk>/", article_detail.as_view(), name="article_detail"),
    path("category/<int:pk>/", articles_by_category.as_view(), name="articles_by_category"),
    path("author/<int:pk>/", articles_by_author.as_view(), name="articles_by_author"),
    path("my-articles", my_Articles.as_view(), name="my-articles"),
    ]