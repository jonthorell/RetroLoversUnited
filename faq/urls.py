
from django.urls import path
from .views import Faq

urlpatterns = [
    path('', Faq.as_view(), name='faq'),
    ]