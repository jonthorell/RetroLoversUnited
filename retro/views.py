

from django.shortcuts import render,redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django import forms
from django.views.generic import TemplateView, ListView, DetailView, View
from retro.forms import CreateArticleForm, EditProfileForm,ContactForm
from retro.forms import CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from retro.models import Link, Article, Category, Comment,User,Profile
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

class EditorRequiredMixin(UserPassesTestMixin):
    '''Class used to restrict access to views where user needs to be editor '''

    def test_func(self):
        return self.request.user.groups.filter(name="Editors").exists()

class AdminRequiredMixin(UserPassesTestMixin):
    '''Class used to restrict access to views where user needs to be admin '''

    def test_func(self):
        return self.request.user.groups.filter(name="admins").exists()

class MemberRequiredMixin(UserPassesTestMixin):
    '''Class used to restrict access to views where user needs to be a member '''

    def test_func(self):
        return self.request.user.groups.filter(name="members").exists()

class ManagerRequiredMixin(UserPassesTestMixin):
    '''Class used to restrict access to views where user needs to be a manager '''

    def test_func(self):
        return self.request.user.groups.filter(name="Managers").exists()

class custom_mixin_kategorimenu(object):
    '''Used to make all the context_data available at all times so the author/categories menues can be populated '''

    # all other classes needs this mixin

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
        except AttributeError:
            context = {}
        context['links'] = Link.objects.all()
        context['categories'] = Category.objects.all()
        context['users'] = User.objects.prefetch_related("groups")
        context['articles'] = Article.objects.prefetch_related("groups")
        context['comments'] = Comment.objects.all()
        context['profiles'] = Profile.objects.all()
        return context

class article_detail(custom_mixin_kategorimenu, DetailView):
    '''Class used for displaying the article '''

    template_name = 'retro/get_article.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(user__id=kwargs.get("pk")).select_related('user').all()
        # return articles to template that has the corresponding kwarg (i.e. the article being displayed)
        return context

class comment_article(MemberRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    '''Class used for commenting article '''

    template_name = 'retro/comment_article.html'
    model = Article
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        # display the form
        context = self.get_context_data()
        form = CommentForm(request.POST)
        return render(
        request,
        "retro/comment_article.html",
        {"form": form, **context},
    )

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # check form is valid and get values from it into variables.
            for arg in kwargs.values():
                article_id=arg
            body = comment_form.cleaned_data.get("body")
            comment_form.name_id=User.id
            
            # add new comment to database
            record = Comment(name_id=request.user.id,body=body,status=1,approved=False,article_id=article_id)
            record.save()

            # notify the user
            messages.info(request, "Your comment has been added.")
            messages.info(request, "It is awaiting approval.")

            # return to article comment was made on
            return HttpResponseRedirect("/article/"+str(article_id))
        else:
            comment_form = CommentForm()

        return render(
            request,
            "retro/comment_article.html",
            {"form": comment_form},
    )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(user__id=kwargs.get("pk")).select_related('user').all()
        # return articles to template that has the corresponding kwarg (i.e. the article being displayed)
        return context

class delete_comment(MemberRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    '''Class used to display the delete comment warning page '''

    template_name = 'retro/delete_comment.html'

class confirm_delete_comment(MemberRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    '''Class used to really delete the comment '''

    template_name = 'retro/confirm_delete_comment.html'
    # template file is not present since it is never really displayed. Another view could have been used but template view is convenient :-)
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        my_id = self.kwargs['pk']
        current_comment = get_object_or_404(Comment, id=my_id)
        context = self.get_context_data(object=current_comment)
        # get current comment
        if current_comment.name_id == request.user.id:
            # if logged in user owns the article, delete it
            art_mess = "Comment is deleted."
            current_comment.delete()
        else:
            # Otherwise, inform the user he/she can not do that
            art_mess = "You do not have permission to delete that comment."
        messages.info(request, art_mess)
        return HttpResponseRedirect("/")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['comments'] = Comment.objects.all()
        return context

class edit_comment(EditorRequiredMixin, custom_mixin_kategorimenu, DetailView):
    '''Class used to edit a comment '''

    template_name = "retro/edit_comment.html"
    model =Comment
    context_object_name="comments"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        my_id = self.kwargs['pk']
        context['comments'] = Comment.objects.filter(id=my_id).all()
        # return comments owned by current user to template
        return context

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        my_id = self.kwargs['pk']
        current_comment = get_object_or_404(Comment, id=my_id)
        context = self.get_context_data(object=current_comment)
        form = CommentForm(instance=current_comment)
        # display form with whatever was in the comment to begin with
        context["form"] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        my_id = self.kwargs['pk']
        current_comment = get_object_or_404(Comment, id=my_id)
        form = CommentForm(data=request.POST, instance=current_comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = current_comment
            comment.approved = False
            comment.save()
            messages.info(request, 'Comment Updated!')
            messages.info(request, 'It needs to be approved again!')
            # update the article and return to main view
            return HttpResponseRedirect("/")
        else:
            form = CommentForm()

        return render(
            request,
            "retro/edit_comment.html",
            {"form": form},
            )

class inactive_account(custom_mixin_kategorimenu, TemplateView):
    '''Class used to display page when you are trying to view the details of an inacctive account (from list all profiles, clicking on an inactive account) '''

    template_name = 'retro/inactive.html'

class articles_by_category(custom_mixin_kategorimenu, DetailView):
    '''Class used to retrieve articles by category '''

    template_name = 'retro/articles_by_category.html'
    model = Category
    context_object_name = 'category'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(category__id=self.kwargs.get("pk")).select_related('category').all()
        # only return articles that belong to the specific category
        return context

class articles_by_author(custom_mixin_kategorimenu, DetailView):
    '''Class used to retrieve articles by author '''

    template_name = 'retro/articles_by_author.html'
    model = User
    context_object_name = 'article'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(user__id=self.kwargs.get("pk")).select_related('user').all()
        # only return articles that belong to the specific editor
        return context

class my_Articles(custom_mixin_kategorimenu, EditorRequiredMixin, TemplateView):
    '''Class used to retrieve articles created by logged in user '''

    template_name = 'retro/my-articles.html'
    model = User
    context_object_name = 'article'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(user__id=self.request.user.id).select_related('user').all()
        # only return articles that belong to the logged in user
        return context

class Index(custom_mixin_kategorimenu, TemplateView):
    '''Class used to display the index page '''

    template_name = 'retro/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.filter(status=1)[:3]
        # return the last three articles to template

        return context

class Contact(custom_mixin_kategorimenu, View):
    '''Class used to display the contact page '''


    def post(self, request, *args, **kwargs):
        # display form
        form = ContactForm(request.POST)
        if form.is_valid():
            # notify user
            messages.info(request, "Thank you. Your response has been logged.")
            # get form values into variables
            req_user = request.POST.get("name")
            req_mess = request.POST.get("mess")
            req_email = request.POST.get("email")
            req_subject = request.POST.get("subject")
            # "change" numerical values into clear-text
            if req_subject == "0":
                req_subj_string = "Technical Issue"
            elif req_subject == "1":
                req_subj_string = "Factual Issue"
            elif req_subject == "2":
                req_subj_string = "Dead link or missing image"
            elif req_subject == "3":
                req_subj_string = "Suggestion for accessability"
            elif req_subject == "4":
                req_subj_string = "Suggestion for new idea"
            elif req_subject == "5":
                req_subj_string = "Suggestion for new link"
            elif req_subject == "6":
                req_subj_string = "General praise/hate"
            else:
                # should never occur
                req_subj_string = "Other"

            # set variables for e-mail.
            subject = 'Mail from RetroLoversUnited'
            message = f'Hi { req_user }, your issue has been received. We will look into it as soon as possible.\nThe message you submitted was { req_mess }. \n\nYou classified it as { req_subj_string }'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [req_email, ]
            # send the mail. Notify the user and return to start page
            send_mail( subject, message, email_from, recipient_list )
            messages.info(request, "Check your e-mail.")
            return HttpResponseRedirect("/")
    def get(self, request, *args, **kwargs):
        # display form
        context = self.get_context_data()
        form = ContactForm(request.POST)
        return render(
        request,
        "retro/contact.html",
        {"form": form, **context},
    )

class FAQ(custom_mixin_kategorimenu, TemplateView):
    '''Class used to display the faq page '''

    template_name = 'faq/faq.html'

class delete_account(MemberRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    '''Class used to display the delete account warning page '''

    template_name = 'retro/delete_account.html'

class delete_article(EditorRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    '''Class used to display the delete article warning page '''

    template_name = 'retro/delete_article.html'
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        my_id = self.kwargs['pk']
        current_article = get_object_or_404(Article, id=my_id)
        context = self.get_context_data(object=current_article)
        # get current article
        return self.render_to_response(context)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.all()
        return context

class confirm_delete_article(MemberRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    '''Class used to really delete the article '''

    template_name = 'retro/confirm_delete_article.html'
    # template file is not present since it is never really displayed. Another view could have been used but template view is convenient :-)
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        my_id = self.kwargs['pk']
        current_article = get_object_or_404(Article, id=my_id)
        context = self.get_context_data(object=current_article)
        # get current article
        if current_article.user_id == request.user.id:
            # if logged in user owns the article, delete it
            art_mess = "Article "+ "\"" + current_article.title+"\"" +" is deleted."
            current_article.delete()
        else:
            # Otherwise, inform the user he/she can not do that
            art_mess = "You do not have permission to delete that article."
        messages.info(request, art_mess)
        return HttpResponseRedirect("/")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['articles'] = Article.objects.all()
        return context

class confirm_delete_user(MemberRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    '''Class used to really delete the user '''

    template_name = 'retro/confirm_delete_user.html'
    # template file is not present since it is never really displayed. Another view could have been used but template view is convenient :-)
    def get(self, request, *args, **kwargs):
        u = request.user
        
        fname = request.user.first_name
        lname = request.user.last_name

        if fname == "Administrator":
            outmess = "The admin account can not be deleted!"
        else:
            outmess = "User " + fname + " " + lname + " is deleted."
            u.delete()
            # delete account
        
        # message the user and return to startpage.
        messages.info(request, outmess)
        return HttpResponseRedirect("/")


class Credits(custom_mixin_kategorimenu, TemplateView):
    '''Class used to display credits page '''

    template_name = 'credits/credits.html'

class About(custom_mixin_kategorimenu, TemplateView):
    '''Class used to display about page '''

    template_name = 'retro/about.html'
    
class Kategories(custom_mixin_kategorimenu, ListView):
    '''Class used to display all categories page '''

    template_name = 'retro/category.html'
    model = Category
    context_object_name = 'categories'

class View_profile(MemberRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    '''Class used to display specific user profile (from list all profiles) '''

    template_name = 'retro/view_profile.html'
    model = Profile
    context_object_name = 'profiles'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['profiles'] = Profile.objects.filter(user__id=kwargs.get("pk")).select_related('user').all()
        # return profile based on kwarg
        return context


class view_my_profile(MemberRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    '''Class used to display currently logged in users profile '''

    template_name = 'retro/view_my_profile.html'
    model =Profile
    context_object_name = 'profiles'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['profiles'] = Profile.objects.filter(user__id=self.request.user.id).select_related('user').all()
        # return logged in user to template
        return context

class edit_profile(MemberRequiredMixin, custom_mixin_kategorimenu, View):
    '''Class used to edit your profile '''

    template_name = 'retro/edit_profile.html'
    model = Profile
    context_object_name = 'profile'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['profiles'] = Profile.objects.filter(user__id=self.request.user.id).select_related('user').all()
        # return the logged in user to template
        return context

    def get(self, request, *args, **kwargs):
        # show the form and pre-fill it with data for currently logged in user
        context = self.get_context_data()
        user_profile = get_object_or_404(Profile, user_id=self.request.user.id)
        form = EditProfileForm(instance=user_profile)
        return render(
            request,
            "retro/edit_profile.html",
            {"form": form, **context},
    )

    def post(self, request, *args, **kwargs):
        user_profile = get_object_or_404(Profile, user_id=self.request.user.id)
        profile_form = EditProfileForm(data=request.POST, instance=user_profile)
        if profile_form.is_valid():
            # if everything is filled in correctly, update current users profile and return to view it
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
    '''Class used to view all profiles '''

    template_name = 'retro/all_profiles.html'
    model = User
    context_object_name = 'profile'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['profiles'] = Profile.objects.select_related('user').all()
        # return all profiles to template
        return context

class List_Users(ManagerRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    '''Class used to list all users in a more "excel-like" way '''

    template_name = 'retro/list_users.html'    

class Links(custom_mixin_kategorimenu, ListView):
    '''Class used to list all suggested links '''

    template_name = 'retro/links.html'
    model = Link
    context_object_name = 'links'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['links'] = Link.objects.all()
        # return all links to template
        return context

class edit_article(EditorRequiredMixin, custom_mixin_kategorimenu, DetailView):
    '''Class used to edit an article '''

    template_name = "retro/edit_article.html"
    model =Article
    context_object_name="articles"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        my_id = self.kwargs['pk']
        context['articles'] = Article.objects.filter(id=my_id).select_related('user').all()
        # return articles owned by current user to template
        return context

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        my_id = self.kwargs['pk']
        current_article = get_object_or_404(Article, id=my_id)
        context = self.get_context_data(object=current_article)
        form = CreateArticleForm(instance=current_article)
        # display form with whatever was in the article to begin with
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
            # update the article and return to article view
            return redirect(my_article)
        else:
            form = CreateArticleForm()

        return render(
            request,
            "retro/edit_article.html",
            {"form": form},
            )


class create_article(EditorRequiredMixin, custom_mixin_kategorimenu, TemplateView):
    '''Class used to create  an article '''

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
            # create article, notify user, and return to homepage
            return redirect("/")
    def get(self, request, *args, **kwargs):
        # create and display empty form
        context = self.get_context_data()
        form = CreateArticleForm(request.POST or None)
        return render(
        request,
        "retro/create_article.html",
        {"form": form, **context},
    )

