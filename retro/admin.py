from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.utils import get_attachment_model
from django.contrib.auth.models import User, Group
from .models import Category,Article,Link,Comment,Profile
from allauth import account

class ArticleAdmin(SummernoteModelAdmin):
    '''Class used to add summernote to adminview '''

    summernote_fields = ('content',)

class ProfileInline(admin.StackedInline):
    '''Class used to aextend the user part of adminview with profile in the same view '''
    model = Profile

class UserAdmin(admin.ModelAdmin):
    '''Class used to aextend the user part of adminview with profile in the same view '''

    model = User
    inlines = [ProfileInline]

#register everything in admin

admin.site.unregister(User)
admin.site.unregister(get_attachment_model())
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Link)
admin.site.register(Comment)
