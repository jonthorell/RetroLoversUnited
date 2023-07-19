
from unicodedata import category
from urllib import request
from django.shortcuts import get_object_or_404,render,redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.urls import reverse
from retro.forms import CreateArticleForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import UserPassesTestMixin
from retro.models import Link, Article, Category, Comment,User,Profile
from django.http import Http404, HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

def listing_links(request, page):
    keywords = Link.objects.all().order_by("name")
    paginator = Paginator(keywords, per_page=5)
    page_object = paginator.get_page(page)
    context = {"page_obj": page_object}
    return render(request, "retro/links.html", context)

def listing_links_api(request):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 5)
    startswith = request.GET.get("startswith", "")
    keywords = Link.objects.filter(
        name__startswith=startswith
    )
    paginator = Paginator(keywords, per_page)
    page_obj = paginator.get_page(page_number)
    data = [{"name": kw.name} for kw in page_obj.object_list]

    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "data": data
    }
    return JsonResponse(payload)

def listing_article_api(request):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 5)
    #startswith = request.GET.get("startswith", "")
    keywords = Article.objects.filter(user_id=15)
        
    paginator = Paginator(keywords, per_page)
    page_obj = paginator.get_page(page_number)
    data = [{"title": kw.title} for kw in page_obj.object_list]

    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "data": data
    }
    return JsonResponse(payload)

def listing_article_by_category(request, page):
    keywords = Article.objects.all().order_by("name")
    paginator = Paginator(keywords, per_page=5)
    page_object = paginator.get_page(page)
    context = {"page_obj": page_object}
    return render(request, "retro/articles_by_category.html", context)

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

def check_user_able_to_see_page(*groups):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            raise PermissionDenied

        return wrapper

    return decorator

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

@check_user_able_to_see_page("Editors")
def create_article(request):
    
    form = CreateArticleForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            Article = form.save(commit=False)
            Article.user_id = request.user.id
            Article.save()
            return redirect("/")
    return render(
        request,
        "retro/create_article.html",
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
        context['articles'] = Article.objects.filter(status=1)[:3]

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
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
         qs = super(Links, self).get_queryset(*args, **kwargs)
         qs = qs.order_by("name")
         return qs

class Thankyou(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/thankyou.html'