# RetroLoversUnited

The aim of this project is to create a community site for everyone that is as obessive with the classic Amiga-computer as I am.

The project is live 
[here](https://retroloversunited.herokuapp.com/)

![mockup-picture](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/mockup.PNG?raw=true?raw=true)

# Background and use-case

The project is for all intents and purposes a community site for that use or is interested in the old Amiga-line of computers.

Designated editors can create and edit articles that may or may not be commented on by ordinary users. Those comments must be approved by a moderator
before they are visible, to prevent spam comments. Users can always edit or delete their comment if they want to. The editors can likewise delete their
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

In the middle you have the main part where you can see list of articles, categories, and interact with them using forms. In the above example, a list of articles
by author Amy Squirrel.

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

Code changes are regularily pushed into that repository using either Github Desktop or the cli command git using:

git add .
git commit -m "commit message"
git push

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



# Bugs

1. Navbar did not list categories for all pages at first. Solved with a mixin to the class-based views
2. Navbar catgories does not work from error pages
3. Problem finding a way of getting the group for the current user. The solution found is not as elegant as I would like, but it works.
4. Got error in devtools for two label lines. Turned out I had forgotten to remove them when the corresponding input field was removed.
5. Bell-drop down created an empty menu if there were no messages. Fixed by moving the ul-container.
6. Spacing issue between author and category menu. DONE
7. Ran into an issue where the view-category-by-category retrieved data from articles instead of categories. Had forgotten to change the Model as well as it was the wrong template type.
8. article-by-author tried to look up category instead of user-id. FIXED. Wrong model.
9. When using view-by-author, the system inexplicable logs the user in as that user??. Fixed. context_view was wrong
10. Faq gets same value from links.description all the time?? Fixed
11. Modal did not close properly on mobile. Seems duplicated ids were responsible, but the browser on the PC was more forgiving. Changed to pop-out instead
12. If user manually changes article id in url bar for editarticle, the display is empty. Works good enough to get the form into place and look into that problem later
13. In edit_article, the kwarg-value was empty when the get-method was available. It worked fine when the get-method was commented-out. Which was a bit of a bummer since the kwarg-value was essential for the logic that checked whether the logged in user was authorized to edit it.
It is fixed, although I am not entirely sure which of the changes that accomplished the task. 

# Todo

1. Clean up css from redundant classes
2. Document models
3. Add comments wherever needed
4. Chnage chip in category to display right avatar and editor-name. DONE
5. Add a credits view. Avatars needs to be added there apart from the rest. DONE

# Other

1. Credits works fine. Should be moved to separate app. DONE
2. Code for pagination adapted from examples at: https://realpython.com/django-pagination/
3. Filter on status. Done in views.py for index. Cant do that for the others since it needs custom code in the template with if/else/for-loops
4. After editing a article, user is redirected to the article view
5. Articles in draft-mode will only be shown in "My articles". It is the only place where it makes sense to show it since no other editor should ever need to see it.

# User classes

Every user belongs to one or more classes of user.

1. Admin. Or superusercs. They can do anything.
2. Editors. Has the ability to create new articles.
3. Members. Can comment on articles (and potentially like articles). Also needed to view profiles.
4. Anonymous users (or not logged in users). Can view articles and comments but not able to comment themselves.
5. Managers. Can see all active and inactive users.

In the issues tracker, webuser is a not logged in user. User is a logged in user.

Members is essentially everyone that is logged in. Admins is the designated superusers. Should also be a member of the editor group.
Editors are those users the admin has added to the editors group. If not a member of the editors group, the create article link disappears.

Bug: the code to retrieve categories from the database threw a "has no attributes" error. Turned out to be a name-mismatch since the name Category was used for a view as well.
Renaming the view name was not the same as the model name.

# Retro Lovers United

This is a site for dedicated users of the now very old Amiga-line of computers where they can get help, tips, and ideas of things to do with their beloved antiques.
Mostly just as a fun hobby, but maybe find some small niche where it can still be useful.

The site is written using HTML, CSS, Django, Python, and MD Bootstrap (Material Design Bootstrap)

# Main Page

When the site is launched, the screen is essentially divided into three parts.

![navbar](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/navbar.PNG?raw=true)

The navbar will of course always be visible no matter where you are on the page. The beachball on the far left takes you back to the homepage (the icon itself comes from the very first
demo released for the Amiga 1000 back in 1985 to showcase some of what it could do). Categories is a drop-down menu where you can choose which category of articles you want to view.
Contact and abouts are just links. Create Article and Admin will not be visible unless you are logged in with sufficient rights.

On the right hand side, the bell indicates whether you have unread notifications (for example, a comment has just been approved). It also acts as a drop-down menu. This icon will also not be shown if you
are not logged in.

The avatar finally will just show a generic one if you are not logged in. Depending on whether you are logged in or out, the menu it offers will offer you either:
* Create Account
* Login

Or:

* Logout

![landing-page](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/landing_page.PNG?raw=true)

The landing page is essentially just a welcome page, but with links to three latest articles added to the site.

![footer](https://github.com/jonthorell/RetroLoversUnited/blob/main/static/images/readme-files/footer.png?raw=true)

The copyright message in the footer will be hidden on smaller screens so the most important thing here is highlighted, the social media icons.
JUst a few that I deemed most suitable for a community site. The URLs for twitter and youtube are search strings into respective platform with
a relevant searchphrase. Github leads straight to this repository.
