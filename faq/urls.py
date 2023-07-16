
from django.urls import path
from .views import Faq

app_name = "faq"

urlpatterns = [
    path('', Faq.as_view(), name='faq'),
    ]