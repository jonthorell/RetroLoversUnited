from pipes import Template
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView

from retro.models import Link, Article, Category, Comment,User

class CustomMixin_kategorimenu(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        context['users'] = User.objects.all()
        context['articles'] = Article.objects.all()
        context['comments'] = Comment.objects.all()

        return context

class Index(CustomMixin_kategorimenu, TemplateView):
    template_name = 'retro/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()[:3]

        return context




class Contact(CustomMixin_kategorimenu, TemplateView):
    template_name = 'retro/contact.html'




class About(CustomMixin_kategorimenu, TemplateView):
    template_name = 'retro/about.html'

    
class Kategory(CustomMixin_kategorimenu, TemplateView):
    template_name = 'retro/category.html'
    

class Create_article(CustomMixin_kategorimenu, TemplateView):
    template_name = 'retro/create_article.html'


class Test(CustomMixin_kategorimenu, TemplateView):
    template_name = 'retro/test.html'


class Links(CustomMixin_kategorimenu, ListView):
    template_name = 'retro/links.html'
    model = Link
    context_object_name = 'links'

    def get_queryset(self, *args, **kwargs):
         qs = super(Links, self).get_queryset(*args, **kwargs)
         qs = qs.order_by("name")
         return qs

class Create_account(CustomMixin_kategorimenu, TemplateView):
    template_name = 'retro/create_account.html'

class Logout(CustomMixin_kategorimenu, TemplateView):
    template_name = 'retro/logout.html'

class Login(CustomMixin_kategorimenu, TemplateView):
    template_name = 'retro/login.html'


class Thankyou(CustomMixin_kategorimenu, TemplateView):
    template_name = 'retro/thankyou.html'



