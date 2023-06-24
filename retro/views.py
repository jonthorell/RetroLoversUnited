from django import template
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test

from retro.models import Link, Article, Category, Comment,User

def is_editor(user):
    return user.groups.filter(name="Editors").exists()

editor_required = user_passes_test(is_editor)

class EditorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Editors").exists()

class custom_mixin_kategorimenu(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        context['users'] = User.objects.all()
        context['articles'] = Article.objects.all()
        context['comments'] = Comment.objects.all()

        return context

class Index(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()[:3]

        return context




class Contact(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/contact.html'




class About(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/about.html'

    
class Kategory(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/category.html'
    

class Create_article(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/create_article.html'

class Edit_profile(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/edit_profile.html'

class View_profile(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/view_profile.html'

class Test(EditorRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/test.html'
    
    


class Links(custom_mixin_kategorimenu, ListView):
    template_name = 'retro/links.html'
    model = Link
    context_object_name = 'links'

    def get_queryset(self, *args, **kwargs):
         qs = super(Links, self).get_queryset(*args, **kwargs)
         qs = qs.order_by("name")
         return qs

class Create_account(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/create_account.html'

class Logout(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/logout.html'

class Login(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/login.html'


class Thankyou(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/thankyou.html'



