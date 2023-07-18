from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.auth.models import User, Group
from .models import Category,Article,Link,Comment,Profile

class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

#class ProfileInline(admin.StackedInline):
#    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    #inlines = [ProfileInline]

# Register your models here.

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Link)
admin.site.register(Comment)
admin.site.register(Profile)
