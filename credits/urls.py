
from django.urls import path
from .views import Credits

app_name = "credits"

urlpatterns = [
    path('', Credits.as_view(), name='credits'),
    ]