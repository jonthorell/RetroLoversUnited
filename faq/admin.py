from django.contrib import admin
from faq.models import Terminology
from django_summernote.admin import SummernoteModelAdmin

class TerminologyAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)

# Register your models here.

admin.site.register(Terminology,TerminologyAdmin)

