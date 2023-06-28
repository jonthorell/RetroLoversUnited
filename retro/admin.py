from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Category,Article,Link,Comment,Profile

class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

# Register your models here.

admin.site.register(Category)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Link)
admin.site.register(Comment)
admin.site.register(Profile)
