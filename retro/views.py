from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

class Index(TemplateView):
    template_name = 'retro/index.html'

class Links(TemplateView):
    template_name = 'retro/links.html'

class Contact(TemplateView):
    template_name = 'retro/contact.html'

class About(TemplateView):
    template_name = 'retro/about.html'
    
class Category(TemplateView):
    template_name = 'retro/category.html'
