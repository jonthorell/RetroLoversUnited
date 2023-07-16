
from unicodedata import category
from django.shortcuts import get_object_or_404,render
from django.views.generic import TemplateView, ListView, DetailView
from django.urls import reverse
from retro.forms import CreateArticleForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import UserPassesTestMixin
from retro.models import Link, Article, Category, Comment,User,Profile

class EditorRequiredMixin(UserPassesTestMixin):
    # Class used to restrict access to views where user needs to be editor
    def test_func(self):
        return self.request.user.groups.filter(name="Editors").exists()

class AdminRequiredMixin(UserPassesTestMixin):
    # Class used to restrict access to views where user needs to be admin
    def test_func(self):
        return self.request.user.groups.filter(name="admins").exists()

class MemberRequiredMixin(UserPassesTestMixin):
    # Class used to restrict access to views where user needs to be member
    def test_func(self):
        return self.request.user.groups.filter(name="members").exists()

class ManagerRequiredMixin(UserPassesTestMixin):
    # Class used to restrict access to views where user needs to be manager
    def test_func(self):
        return self.request.user.groups.filter(name="Managers").exists()

class custom_mixin_kategorimenu(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        context['users'] = User.objects.all()
        context['articles'] = Article.objects.all()
        context['comments'] = Comment.objects.all()
        context['profiles'] = Profile.objects.all()

        return context

def create2(request):
    form = CreateArticleForm(request.POST or None)

    return render(
        request,
        "retro/create_article2.html",
        {"form": form},
    )


class article_detail(custom_mixin_kategorimenu, DetailView):
    template_name = 'retro/get_article.html'
    model = Article
    context_object_name = 'article'

class articles_by_category(custom_mixin_kategorimenu, DetailView):
    template_name = 'retro/articles_by_category.html'
    model = Category
    context_object_name = 'category'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(category__id=self.kwargs.get("pk")).select_related('category').all()
        return context

class articles_by_author(custom_mixin_kategorimenu, DetailView):
    template_name = 'retro/articles_by_author.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(user__id=self.kwargs.get("pk")).all()
        return context

class Index(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.all()[:3]

        return context



class Contact(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/contact.html'

class FAQ(custom_mixin_kategorimenu, TemplateView):
    template_name = 'faq/faq.html'

class Credits(custom_mixin_kategorimenu, TemplateView):
    template_name = 'credits/credits.html'




class About(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/about.html'

    
class Kategories(custom_mixin_kategorimenu, ListView):
    template_name = 'retro/category.html'
    model = Category
    context_object_name = 'categories'


    

class Create_article(EditorRequiredMixin,custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/create_article.html'

class Edit_profile(MemberRequiredMixin,custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/edit_profile.html'

class View_profile(MemberRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/view_profile.html'
    model = Profile
    context_object_name = 'profile'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(category__id=self.kwargs.get("pk")).select_related('category').all()
        return context

class Test(AdminRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/test.html'

    
class List_Users(ManagerRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/list_users.html'    


class Links(custom_mixin_kategorimenu, ListView):
    template_name = 'retro/links.html'
    model = Link
    context_object_name = 'links'

    def get_queryset(self, *args, **kwargs):
         qs = super(Links, self).get_queryset(*args, **kwargs)
         qs = qs.order_by("name")
         return qs

class Editor(custom_mixin_kategorimenu, TemplateView):
    template_name='retro/editor.html'

class Thankyou(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/thankyou.html'