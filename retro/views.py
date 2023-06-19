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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        return context


class Contact(TemplateView):
    template_name = 'retro/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        return context



class About(TemplateView):
    template_name = 'retro/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        return context
    
class Kategory(TemplateView):
    template_name = 'retro/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        return context

class Create_article(TemplateView):
    template_name = 'retro/create_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        return context

class Test(TemplateView):
    template_name = 'retro/test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        return context

class Links(ListView):
    template_name = 'retro/links.html'
    model = Link
    context_object_name = 'links'

    def get_queryset(self, *args, **kwargs):
         qs = super(Links, self).get_queryset(*args, **kwargs)
         qs = qs.order_by("name")
         return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        return context

class Create_account(TemplateView):
    template_name = 'retro/create_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        return context

class Logout(TemplateView):
    template_name = 'retro/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        return context

class Login(TemplateView):
    template_name = 'retro/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        return context

class Thankyou(TemplateView):
    template_name = 'retro/thankyou.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        return context


