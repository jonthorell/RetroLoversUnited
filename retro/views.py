from pipes import Template
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView

from retro.models import Link, Article, Category, Comment


class Index(ListView):
    template_name = 'retro/index.html'
    model = Article
    context_object_name = "articles"

    def get_queryset(self, *args, **kwargs):
        qs = super(Index, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-created_on")[:3]
        return qs


class Contact(TemplateView):
    template_name = 'retro/contact.html'



class About(TemplateView):
    template_name = 'retro/about.html'
    
class Category(ListView):
    template_name = 'retro/category.html'
    model = Category
    context_object_name = "categories"

    def get_queryset(self, *args, **kwargs):
        qs = super(Category, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("name")
        return qs

class Create_article(TemplateView):
    template_name = 'retro/create_article.html'

class Test(TemplateView):
    template_name = 'retro/test.html'

class Links(ListView):
    template_name = 'retro/links.html'
    model = Link
    context_object_name = 'links'

    def get_queryset(self, *args, **kwargs):
         qs = super(Links, self).get_queryset(*args, **kwargs)
         qs = qs.order_by("name")
         return qs

class Create_account(TemplateView):
    template_name = 'retro/create_account.html'

class Logout(TemplateView):
    template_name = 'retro/logout.html'

class Login(TemplateView):
    template_name = 'retro/login.html'

class Thankyou(TemplateView):
    template_name = 'retro/thankyou.html'


