from django.views.generic import TemplateView
from django.shortcuts import render
from retro.models import Link, Article, Category, Comment,User,Profile
from faq.models import  Terminology

# Create your views here.

class custom_mixin_kategorimenu(object):
    '''Used to make all the context_data available at all times so the author/categories menues can be populated '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        context['users'] = User.objects.all()
        context['articles'] = Article.objects.all()
        context['comments'] = Comment.objects.all()
        context['profiles'] = Profile.objects.all()

        return context

class Faq(custom_mixin_kategorimenu, TemplateView):
    ''' Class used for the faq view '''
    template_name = 'faq/faq.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['faqs'] = Terminology.objects.all()
        # return all rows to the template

        return context