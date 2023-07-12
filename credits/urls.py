
from django.urls import path
from .views import Credits

urlpatterns = [
    path('', Credits.as_view(), name='credits'),
    ]