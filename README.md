# RetroLoversUnited

The aim of this project is to create a community site for everyone that is as obessive with the classic Amiga-computer as I am.

The project is live 
[here](https://retroloversunited.herokuapp.com/)

![mockup-picture](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/mockup.PNG?raw=true?raw=true)

# Background and use-case

The project is for all intents and purposes a community site for that use or is interested in the old Amiga-line of computers.

Designated editors can create and edit articles that may or may not be commented on by ordinary users. Those comments must be approved by a moderator
before they are visible (although articles do not, editors are presumed to be trustworthy), to prevent spam comments. Users can always edit or delete 
their comment if they want to. The editors can likewise delete their
articles (although if they do that, the associated comments will be deleted as well).

Everyone can at any time delete their account, but the same caveat applies. Associated articles (in case user was an editor) and commments will
be deleted as well.

The screen is divided into three parts.

At the top,

![navbar](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/navbar.PNG?raw=true)

Authors and Categories are pop-down menues that will show shortcuts to all articles by a given editor, or articles
in a given category (i.e. Hardware). Contact, About, FAQ (essentially a "list" of vocabulary specific to the Amiga), & Credits
are always shown. Create Article, Admin, and List Active Users are shown depending on whether the logged in user has the right
to use the function.

The icon on the far right controls account related functions such as sign up, login, logout, edit profile, & delete account.

In the middle you have the main part where you can see list of articles, categories, and interact with them using forms. In this example, a list of articles
by author Amy Squirrel. As a sidenote, most editors in the authors menu should be recognizable by Amiga-users.

![middle-part](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/landing_page.PNG?raw=true)

And finally, at the bottom. A footer with copyright information and links to social media.

![footer](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/footer.png?raw=true)

# Design considerations (visual).

1. Colors and other graphical elements have been "stolen" or mimicked from AmigaOS as much as possible. 
2. The beachball at the top-left is a sort-of unofficial logo.
3. The grey background is the default background color of the GUI.
4. The navbar uses the same white as the AmigaOS menubar.
5. The black text is the default font-color.
6. The orange text comes from the "fuel-gauge" that indicates how full a disk is (from an earlier version of AmigaOS).
7. The black background and the blinking graphics on the 403 page is how the Amiga indicates it has run into a dead-end software failure.
8. The site should be fully responsive.

# Technologies used

1. HTML
2. CSS (with classes from MaterializeBootstrap as well as my own)
3. Javascript
4. Django
5. Python
6. Git (from within Visual Studio), pushed to GitHub. UserStories and Kanban board is also hosted at GitHub.
7. Postgres SQL

NOTE: timeline in Agileproject. Made an initial mistake there so had start over from scratch. The dates are therefor not necessarily completely accurate. Also, I probably should have set the different
iterations without due-dates. See further under lessons learned.

# Design considerations (code)

1. Since it is a django-project, configuation is done in settings.py, forms.py, & urls.py
2. The project consists of three apps. One main where the main logic takes place. And two subapps, faq and credits. Point one applies here as well.
3. The main code is in views.py and "scattered" in the django template files as well such as the articles_by_author file. In the latter case it stuff like this:
```django
{% if profile.user.is_active %}
{% endif %
```
4. Comments are used in both the python code and the template files. In the latter case, it is html-comments surrounded by the django comment-tags. The purpose for doing it twice is that the html-comment sticks out color-wise in the code editor and the django-tags make sure commens are not visible in view source.
5. Everything is based upon class-based views rather than being function based.

# Design considerations (user classes)

Every user belongs to one or more classes of user. This is implemented using django groups.

1. Admin. Or superusers. They can do anything.
2. Editors. Has the ability to create new articles.
3. Members. Can comment on articles. Also needed to view profiles. When someone sign up, they are automatically added to this group. If they need to be in another group (say editors) an admin has to add them there manually.
4. Anonymous users (or not logged in users). Can view articles and comments but not able to comment themselves.
5. Managers. Can see all active and inactive users.

In the issues tracker, webuser is a not logged in user. User is a logged in user.

# Deployment

All coding takes place in Visual Studio and regularily pushed to the repo at GitHub. There are some "hidden" environmental variables in a file called env.py that is excluded from git
pushes. Those variables are used when running locally. The variables in question are:

* DATABASE_URL
* SECRET_KEY
* CLOUDINARY_URL
* EMAIL_HOST_PASSWORD
* EMAIL_HOST_USER

# Deployment to Heroku

In order to deploy something to Heroku, several steps needs to be taken care of.

This is taken for granted that the project is already hosted at GitHub.

Code changes are regularily pushed into that repository using either Visual Studio or the cli command git using:

1. git add .
2. git commit -m "commit message"
3. git push

The steps for deployment to Heroku are:

1. Create an account at Heroku.
2. Create an app in Heroku, with a unique name and a region
3. Under settings, create an environment variable with the name PORT and value of 8000. Duplicate the variables under deployment here as well.
4. In your development environment, do: pip freeze > requirements.txt to add the requirements needed to build the project at heroku.
Things installed, if any, locally will be added to the requirements file, to make sure everything necessary will be available when deployed.
This might include things not necessarily referenced, but it will make sure the build will be complete.
5. Make sure there's a file named Procfile in the root of your repo with this line: web: gunicorn retroloversunited.wsgi
6. Under deployment, connect the github account to the heroku-account
7. Under deployment method, connect the app to the correct github repository
8. Decide if you want the deployment to be automatic or manual. That is a matter of preference. For now, I have opted to make it manual.

# Database design

Since the entire site is built around three apps, there is a possibility to use models in three different places.

App: FAQ

Uses one very simple model called Terminology. It has four fields (5 if you count the automatically created id/pk field).

* Name: Charfield, max 40 characters in length. Can not be blank and must be unique. It must be unique because it is used as a title in the display and I do not want to confuse the user with having the same name twice or more.
* Created_on: Datefield, is automatically filled in.
* Slug: filled automatically using the third-party django-autoslug package. In the end I ended up not using slugs to create more intuiative urls since I could not quite get it to work the way I wanted, but left the field if I want to extend the site later on.
* Description: Charfield, max length 3000, must not be empty. Used to provide the "meat" of the terminology so the user can get more information.

There are no relations to other models. Also, this particular model needs to be populated from django-admin.

The output of this model looks like this:

![model-faq](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/faq-model.PNG)

App: Credits

Does not use a model.

App: Retro


# Bugs encountered and fixed

1. Navbar did not list categories for all pages at first. Solved with a mixin to the class-based views
2. The code to retrieve categories from the database threw a "has no attributes" error. Turned out to be a name-mismatch since the name Category was used for a view as well.
Renaming the view name was not the same as the model name fixed the problem.
3. Problem finding a way of getting the group for the current user. The solution found is not as elegant as I would like, but it works.
4. Got error in devtools for two label lines. Turned out I had forgotten to remove them when the corresponding input field was removed.
5. Change chip in category to display right avatar and editor-name. Fixed.
6. Spacing issue between author and category menu. Fixed.
7. Ran into an issue where the view-category-by-category retrieved data from articles instead of categories. Had forgotten to change the Model as well as it was the wrong template type.
8. article-by-author tried to look up category instead of user-id. Fixed. Accidentally used the wrong model.
9. When using view-by-author, the system inexplicable logs the user in as that user??. Fixed. context_view was wrong
10. Faq gets same value from links.description all the time?? Fixed, the for-loop retrieved data from the wrong place.
11. Modal did not close properly on mobile. Seems duplicated ids were responsible, but the browser on the PC was more forgiving. Changed to pop-out instead
12. If user manually changes article id in url bar for editarticle, the display is empty. Works good enough to get the form into place and look into that problem later. Fixed.
13. In edit_article, the kwarg-value was empty when the get-method was available. It worked fine when the get-method was commented-out. Which was a bit of a bummer since the kwarg-value was essential for the logic that checked whether the logged in user was authorized to edit it. Fixed.
14. The categories and authors menues in some situations failed to display their content. Worked in most cases though. I am not enirely sure why the solution works. Since the start I have used a custom mixin in every other class
	to make sure the navbar gets access to everything it needs. But from certain views it did not.
	
	In the mixin, the try/except construct was added.

```django
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
```		
		
In the "offending" class, the line below the comment and the **context line at the bottom was added.

```django
def get(self, request, *args, **kwargs):
        # display the form
        context = self.get_context_data()
        form = CommentForm(request.POST)
        return render(
        request,
        "retro/comment_article.html",
        {"form": form, **context},
    )	
```		
## Remaining bugs

None known.

# Notes

1. Credits worked fines as is, but decided to move it and the FAQ to separate apps.
2. Code for pagination uses classes from Materialize Bootstrap.
3. Filter on status. Done in views.py for index. Can't do that for the others since it needs custom code in the template with if/else/for-loops
4. Articles in draft-mode will only be shown in "My articles". It is the only place where it makes sense to show it since no other editor should ever need to see it.

# Testing

Testing has been done manually in selecting the different menu entries, trying to get an unauthorized user getting the possibility to edit something, and trying to get user
A to be able to edit/delete something belonging to user B, among other things. I have not been able to trigger errors
of that sort but get the proper error message as expected.

## Lighthouse

One Lighthouse screenshot per view. In All cases Lighthouse complains about missing explicit size-tags (not surprising since it is in a header.html that in turn is included in base.html). However,
the error is misleading. The width and height attributes are set using css-classes which lighthouse does not pick up upon.

Lighthouse also complains about things I can not do much about without re-rewriting the front-end framework that is being used (Materialize bootstrap).

In this example for instance.

![lighthouse-error](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/error-lh.PNG?raw=true)

The buttons are created on the fly by the classname added and the data-* fields needed for the class to work. In some cases there might be work-arounds for it, but not always.

It also complains about some issues logged:

![lighthouse-error2](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/issues_logged.PNG?raw=true)

Those issues turned out to be cookie-related stuff coming from cloudinary, nothing much I can do about that as far as I can tell.

![coookies](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/cookies-cloudinary.PNG?raw=true)

When viewing an article, it complains about explicit width and height not set. It seems like summernote does not set those values when you upload an image using that component.

![summernote-no-explicit-width](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/no-explicit-summernote.PNG?raw=true)

Index

![index](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/index.PNG?raw=true)

View-by-author

![view-by-author](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/by-author.PNG?raw=true)

View-by-category

![view-by-category](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/by-category.PNG?raw=true)

All-categoeies

![all-categories](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/all_categories.PNG?raw=true)

Links

![links](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/links.PNG?raw=true)

Contact

![contact](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/contact.PNG?raw=true)

About

![about](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/about.PNG?raw=true)

FAQ

![faq](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/faq.PNG?raw=true)

Credits

![credits](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/credits.PNG?raw=true)

Create-article

![create-article](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/create_article.PNG?raw=true)

Edit-article

![edit-article](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/edit_article.PNG?raw=true)

Delete article

![delete-article](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/delete_article.PNG?raw=true)

View article

![view-article](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/get_article.PNG?raw=true)

My articles

![my-articles](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/my-articles.PNG?raw=true)

All profiles

![all-profiles](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/all_profiles.PNG?raw=true)

View my profile

![my-profile](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/view_my_profile.PNG?raw=true)

Edit profile

![edit-profile](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/edit_profile.PNG?raw=true)

Delete account

![delete-account](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/delete_account.PNG?raw=true)

Inactive account

![inactive-account](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/inactive_account.PNG?raw=true)

List users

![list-users](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/list_users.PNG?raw=true)

Comment article

![comment-article](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/comment_article.PNG?raw=true)

Delete comment

![delete-comment](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/delete_comment.PNG?raw=true)

Edit comment

![edit-comment](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/edit_comment.PNG?raw=true)

As can be seen, the values from lighthouse are fairly consistant across the board. But see above for a partial explantion of what could potentially
lower the scores. Some of them are, as far as I can tell, out of my control at this point. I could have found out about those issues earler on and
found ways to fix it, but I did not spot the issues in time.

That being said, there is one thing that I could fix:

Contrast problem

![contrast-problem](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/lighthouse/contrast.PNG?raw=true)

Now, I am not sure how lighthouse determines the contast issue. However it does it, I decided not to fix the issue. Why? Partially because if someone like me with a notoriously bad sight
can read the text without problems it can not be that big of an issue. Which, of couse, is subjective. The other reason is also subjective, but since the site is about the Amiga I want the color-scheme
to reflect it as close as possible, warts and all. 

## HTML validation

The different pages have been validated through 

[validator](https://validator.w3.org)

In order to not get complaints about Django-tags, the "view source" output for every page has been pasted into the validator. 

I got the following result for the pages listed below (listed this way to make it more digestable).

![html-checker](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/html-checker.PNG?raw=true)

* Index
* By author
* All categories
* By Category
* Links
* 
* 



# Lessons learned

* Setting deadlines on Agile milestones was not a good idea when you are new to both the Agile methodology (besides, the Agile methodology works better if it is a team responsible and not a sole developer) and trying to learn the Django framework at the same time. Especially since I can not work on the project full-time due to other things on my plate. Having just the user stories and the project board would have been sufficient.

* In retrospect, I also would have added more logic in the views.py file where it belongs instead of in the templates. It would make everything more manageable and a better split between layout/logic.

* As always, I tend to make the project too big in scope.



