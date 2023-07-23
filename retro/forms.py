
from allauth.account.forms import SignupForm
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from django.contrib.auth.models import User, Group
from django import forms
from django.utils.translation import gettext as _
from retro.models import Category, Profile,Article

 
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,)

    def __init__(self, *args, **kwargs):
       super(SignupForm, self).__init__(*args, **kwargs)
       self.fields['first_name'].widget = forms.TextInput(attrs={'placeholder': 'Enter first name'})
       self.fields['last_name'].widget = forms.TextInput(attrs={'placeholder': 'Enter last name'})
       self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
       self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Password again'})

    def save(self, request):
        
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user_group = "members"
        g = Group.objects.get(name=user_group)
        user.groups.add(g)
        user.save()
        full_name=user.first_name+" "+user.last_name
        short="Short description of "+full_name
        description="Description of "+full_name
        computer="Describe your computer setup here."
        user_id=user.id
        new = Profile(short_description=short,description=description,user_id=user_id,computer=computer)
        new.save()
        return user

class EditProfileForm(forms.ModelForm):
    description = forms.CharField(
        required = True,
        widget = forms.widgets.TextInput(
            attrs={
                "placeholder": "Description of user",
                "class": "form-control form-control-sm",
                }
            ),
            label="",
        )
    computer = forms.CharField(
        required = True,
        widget = forms.widgets.Textarea(
            attrs={
                "placeholder": "Computer setup",
                "class": "form-control form-control-sm",
                }
            ),
            label="",
        )

    class Meta:
        model = Profile
        widgets = {
            'foo': SummernoteWidget(),
            'bar': SummernoteInplaceWidget(),
        } 
        exclude = ("short_description", "user", "avatar",)

class CreateArticleForm(forms.ModelForm):
    foo = SummernoteTextField()
    
    content = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Main content of article",
                "class": "form-control form-control-sm",
            }
        ),
        label="",
    )

    title = forms.CharField(
        required=True,
        widget = forms.widgets.TextInput(
            attrs={
                 "placeholder": "Title of article",
                "class": "form-control form-control-sm validate",
                }
            ),
        label="",
    )

    excerpt = forms.CharField(
        required=True,
        widget = forms.widgets.TextInput(
            attrs={
                 "placeholder": "Excerpt of article",
                "class": "form-control form-control-sm validate",
                }
            ),
        label="",
    )


    class Meta:
        model = Article
        widgets = {
            'foo': SummernoteWidget(),
            'bar': SummernoteInplaceWidget(),
        } 
        exclude = ("user", "featured_image")