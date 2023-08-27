
from . import views
from django.urls import path
from .views import Index, Links,Contact, About, Kategories, confirm_delete_user, edit_profile
from .views import View_profile,List_Users,article_detail,articles_by_category,articles_by_author
from .views import create_article,my_Articles,view_my_profile,all_profiles, inactive_account
from .views import edit_article,delete_account, delete_article, confirm_delete_article
from .views import comment_article,delete_comment,confirm_delete_comment

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('links', Links.as_view(), name='links'),
    path('contact',Contact.as_view(), name='contact'),
    path('inactive_account', inactive_account.as_view(), name='inactive_account'),
    path('about', About.as_view(), name='about'),
    path('category', Kategories.as_view(), name='Kategories'),
    path('create_article', create_article.as_view(), name='create_article'),
    path('edit_article/<int:pk>', edit_article.as_view(), name='edit_article'),
    path('edit_profile', edit_profile.as_view(), name='edit_profile'),
    path("view_profile/<int:pk>/", View_profile.as_view(), name='view_profile'),
    path("view_profile", View_profile.as_view(), name='view_profile'),
    path("view_my_profile", view_my_profile.as_view(), name='view__my_profile'),
    path("all_profiles", all_profiles.as_view(), name="all_profiles"),
    path('list_users', List_Users.as_view(), name='list_users'),
    path("article/<int:pk>/", article_detail.as_view(), name="article_detail"),
    path("category/<int:pk>/", articles_by_category.as_view(), name="articles_by_category"),
    path("author/<int:pk>/", articles_by_author.as_view(), name="articles_by_author"),
    path("my-articles", my_Articles.as_view(), name="my-articles"),
    path("delete_account", delete_account.as_view(), name="delete_account"),
    path("confirm_delete_user/", confirm_delete_user.as_view(), name="confirm_delete_user"),
    path('delete_article/<int:pk>/', delete_article.as_view(), name='delete_article'),
    path('confirm_delete_article/<int:pk>/', confirm_delete_article.as_view(), name='confirm_delete_article'),
    path('comment_article/<int:pk>/', comment_article.as_view(), name='comment_article'),
    path('delete_comment/<int:pk>/', delete_comment.as_view(), name='delete_comment'),
    path('confirm_delete_comment/<int:pk>/', confirm_delete_comment.as_view(), name='confirm_delete_comment'),
    ]