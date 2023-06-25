from django.contrib import admin
from .models import Category,Article,Link,Comment,Profile

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class CommentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

#class ProfileAdmin(admin.ModelAdmin):
#    prepopulated_fields = {"slug": ("username",)}

# Register your models here.

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Link)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile)
