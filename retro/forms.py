from allauth.account.forms import SignupForm
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.auth.models import User, Group
from django import forms

class CreateForm(forms.Form):
    foo = forms.CharField(widget=SummernoteWidget())

 
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):
        
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user_group = "members"
        g = Group.objects.get(name=user_group)
        user.groups.add(g)
        user.save()
        return user