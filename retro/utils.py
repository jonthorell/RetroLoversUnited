
from retro.models import Link, Article, Category, Comment,User,Profile
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

def check_user_able_to_see_page(*groups):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            raise PermissionDenied

        return wrapper

    return decorator