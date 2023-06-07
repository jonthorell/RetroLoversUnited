from django.shortcuts import render
from django.views import generic, View



# Create your views here.

class home(generic.ListView):
    template_name = "index.html"
