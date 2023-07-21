from django.core.paginator import Paginator
from retro.models import Link, Article, Category, Comment,User,Profile
from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

def listing_links(request, page):
    keywords = Link.objects.all().order_by("name")
    paginator = Paginator(keywords, per_page=5)
    page_object = paginator.get_page(page)
    context = {"page_obj": page_object}
    return render(request, "retro/links.html", context)

def listing_links_api(request):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 5)
    startswith = request.GET.get("startswith", "")
    keywords = Link.objects.filter(
        name__startswith=startswith
    )
    paginator = Paginator(keywords, per_page)
    page_obj = paginator.get_page(page_number)
    data = [{"name": kw.name} for kw in page_obj.object_list]

    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "data": data
    }
    return JsonResponse(payload)

def listing_article_api(request):
    
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 5)
    #startswith = request.GET.get("startswith", "")
    keywords = Article.objects.filter(category_id=15)
        
    paginator = Paginator(keywords, per_page)
    page_obj = paginator.get_page(page_number)
    data = [{"title": kw.title} for kw in page_obj.object_list]

    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "data": data
    }
    return JsonResponse(payload)

def listing_article_by_category(request, page):
    keywords = Article.objects.all().order_by("name")
    paginator = Paginator(keywords, per_page=5)
    page_object = paginator.get_page(page)
    context = {"page_obj": page_object}
    return render(request, "retro/articles_by_category.html", context)

def check_user_able_to_see_page(*groups):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            raise PermissionDenied

        return wrapper

    return decorator