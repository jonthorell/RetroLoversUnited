
from django.shortcuts import render,redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django import forms
from django.views.generic import TemplateView, ListView, DetailView, View
from retro.forms import CreateArticleForm, EditProfileForm,ContactForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from retro.models import Link, Article, Category, Comment,User,Profile
from django.urls import reverse
from django.contrib import messages

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

class article_detail(custom_mixin_kategorimenu, DetailView):
    template_name = 'retro/get_article.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(user__id=kwargs.get("pk")).select_related('user').all()
        return context

class inactive_account(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/inactive.html'

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
    context_object_name = 'article'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(user__id=self.kwargs.get("pk")).select_related('user').all()
        return context

class my_Articles(custom_mixin_kategorimenu, EditorRequiredMixin, TemplateView):
    template_name = 'retro/my-articles.html'

    model = User
    context_object_name = 'article'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(user__id=self.request.user.id).select_related('user').all()
        return context

class Index(custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(status=1)[:3]

        return context

class Contact(custom_mixin_kategorimenu, DetailView):
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.info(request, "Thank you. Your response has been logged.")
            return HttpResponseRedirect("/")
    def get(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        return render(
        request,
        "retro/contact.html",
        {"form": form},
    )

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

class View_profile(MemberRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/view_profile.html'
    model = Profile
    context_object_name = 'profiles'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['profiles'] = Profile.objects.filter(user__id=kwargs.get("pk")).select_related('user').all()
        # context['profiles'] = Profile.objects.filter(user_id__id=self.kwargs.get("pk")).select_related('user').all()
        return context


class view_my_profile(MemberRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/view_my_profile.html'
    model =Profile
    context_object_name = 'profiles'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['profiles'] = Profile.objects.filter(user__id=self.request.user.id).select_related('user').all()
        return context

class edit_profile(MemberRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/edit_profile.html'
    model = Profile
    context_object_name = 'profile'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['profiles'] = Profile.objects.filter(user__id=self.request.user.id).select_related('user').all()
        return context

    def get(self, request, *args, **kwargs):
        user_profile = get_object_or_404(Profile, user_id=self.request.user.id)
        form = EditProfileForm(instance=user_profile)
        return render(
            request,
            "retro/edit_profile.html",
            {"form": form},
    )

    def post(self, request, *args, **kwargs):
        
        user_profile = get_object_or_404(Profile, user_id=self.request.user.id)
        profile_form = EditProfileForm(data=request.POST, instance=user_profile)
        if profile_form.is_valid():
            my_profile = profile_form.save(commit=False)
            my_profile.post = user_profile
            my_profile.save()
            messages.info(request, "Your profile has been updated.")
            return HttpResponseRedirect("/view_my_profile")
        else:
            profile_form = EditProfileForm()

        return render(
            request,
            "retro/edit_profile.html",
            {"form": profile_form},
    )

class all_profiles(MemberRequiredMixin, custom_mixin_kategorimenu, TemplateView):
     template_name = 'retro/all_profiles.html'
     model = User
     context_object_name = 'profile'

     def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['profiles'] = Profile.objects.select_related('user').all()
        return context

class Test(AdminRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/test.html'

class List_Users(ManagerRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    template_name = 'retro/list_users.html'    

class Links(custom_mixin_kategorimenu, ListView):
    template_name = 'retro/links.html'
    model = Link
    context_object_name = 'links'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['links'] = Link.objects.all()
        return context

class article_like(View):

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=request.user.id)

        if article.ratings.filter(id=request.user.id).exists():
            article.ratings.remove(request.user)
        else:
            article.ratings.add(request.user)

        return HttpResponseRedirect(reverse('article_detail', args=[id]))

class edit_article(EditorRequiredMixin, custom_mixin_kategorimenu, DetailView):
    template_name = "retro/edit_article.html"
    model =Article
    context_object_name="articles"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        my_id = self.kwargs['pk']
        context['articles'] = Article.objects.filter(id=my_id).select_related('user').all()
        return context

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        my_id = self.kwargs['pk']
        current_article = get_object_or_404(Article, id=my_id)
        context = self.get_context_data(object=current_article)
        form = CreateArticleForm(instance=current_article)
        context["form"] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        my_id = self.kwargs['pk']
        current_article = get_object_or_404(Article, id=my_id)
        form = CreateArticleForm(data=request.POST, instance=current_article)
        if form.is_valid():
            my_article = form.save(commit=False)
            my_article.post = current_article
            my_article.save()
            messages.info(request, 'Article Updated!')
            return redirect(my_article)
        else:
            form = CreateArticleForm()

        return render(
            request,
            "retro/edit_article.html",
            {"form": form},
            )


class create_article(EditorRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    template_name = "retro/create_article.html"
    model = Article
    context_object_name="articles"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(user_id=self.request.user.id).select_related('user').all()
        context['categories'] = Category.objects.all()
        
        return context

    def post(self, request, *args, **kwargs):
        form = CreateArticleForm(request.POST or None)
        if form.is_valid():
            Article = form.save(commit=False)
            Article.user_id = request.user.id
            Article.save()
            messages.info(request, "Article has been created.")
            return redirect("/")
    def get(self, request, *args, **kwargs):
        form = CreateArticleForm(request.POST or None)
        return render(
        request,
        "retro/create_article.html",
        {"form": form},
    )

