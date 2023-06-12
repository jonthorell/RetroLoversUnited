from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView

from retro.models import Link, Article


class Index(ListView):
    template_name = 'retro/index.html'
    model = Article
    context_object_name = "articles"

    def get_queryset(self, *args, **kwargs):
        qs = super(Index, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-updated_on")[:3]
        return qs


#class Links(TemplateView):
#    template_name = 'retro/links.html'

class Contact(TemplateView):
    template_name = 'retro/contact.html'

class About(TemplateView):
    template_name = 'retro/about.html'
    
class Category(TemplateView):
    template_name = 'retro/category.html'

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

