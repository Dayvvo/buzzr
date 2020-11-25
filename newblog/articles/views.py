from django.shortcuts import render, redirect
from .models import Article
from .models import Contact
from .forms import Contactform, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader, Context
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.views.generic import View
import time, math
# Create your views here.


def render_user(request):
    user1 = request.user
    return {'user1': user1}


def index2(request, slug):
    int_value = int(slug) * 6
    first_value = (int(slug)-1) * 6
    articles = Article.objects.all()
    trending = Article.objects.order_by('views').reverse()[:6]
    count = math.floor(articles.count() / 6)
    if articles.count() % 6 == 0:
        count_array = [i for i in range(1, count+1)]
    else:
        count_array = [i for i in range(1, count+2)]
    if int_value > articles.count():
        # article_query = Article.objects.order_by('date')[:int_value][::-1]
        article_query = articles.order_by('date').reverse()[first_value:articles.count()]
    else:
        # article_query = Article.objects.order_by('date').reverse()[first_value:int_value]
        article_query = Article.objects.order_by('date').reverse()[first_value:int_value]
    next_location = request.POST.get('next')
    form = Contactform(request.POST or None)
    if form.is_valid():
        form.save()
        if next_location:
            return redirect(next)
        return redirect('/index/')
    context = {
        'form': form,
        'articles': article_query,
        'genres': 'News',
        'article_query': count_array,
        'index': 'index',
        'trending': trending
    }

    return render(request, 'index.html', context)


def index(request):
    articles = Article.objects.order_by('date').reverse()
    if articles.count() > 6:
        articles_shave = articles[:6]
    count = math.floor(articles.count() / 6)
    trending = Article.objects.order_by('views').reverse()[:6]
    if articles.count() % 6 == 0:
        count_array = [i for i in range(1, count+1)]
    else:
        count_array = [i for i in range(1, count+2)]
    next_location = request.POST.get('next')
    form = Contactform(request.POST or None)
    if form.is_valid():
        form.save()
        if next_location:
            return redirect(next)
        return redirect('/index/')
    context = {
        'form': form,
        'articles': articles_shave,
        'genres': 'News',
        'article_query': count_array,
        'index': 'index',
        'trending': trending

    }
    return render(request, 'index.html', context)


def category2(request, slug, slug2):
    int_value = int(slug2) * 4
    first_value = (int(slug2)-1) * 4
    articles = Article.objects.filter(genre=slug).order_by('date').reverse()
    trending = Article.objects.order_by('views').reverse()[:6]
    count = math.floor(articles.count() / 4)
    if articles.count() % 4 == 0:
        count_array = [i for i in range(1, count+1)]
    else:
        count_array = [i for i in range(1, count+2)]
    if count <= 1:
        count_array = [i for i in range(1, count+2)]
    if int_value > articles.count():
        article_query = articles[first_value:articles.count()]
    else:
        article_query = articles[first_value:int_value]
    next_location = request.POST.get('next')
    form = Contactform(request.POST or None)
    if form.is_valid():
        form.save()
        if next_location:
            return redirect(next)
        return redirect('/index/')
    context = {
        'form': form,
        'articles': article_query,
        'genres': 'News',
        'article_query': count_array,
        'index': slug,
        'category': 'category',
        'trending': trending

    }

    return render(request, 'index.html', context)


def by_category(request, slug):
    next_location = request.POST.get('next')
    article_set = Article.objects.filter(genre=slug).order_by('date').reverse()[:4]
    if article_set.count() > 4:
        article_set = article_set[:4]
    count = math.floor(article_set.count() / 2)
    trending = Article.objects.order_by('views').reverse()
    trending = Article.objects.order_by('views').reverse()[:5]
    if article_set.count() % 3 == 0:
        count_array = [i for i in range(1, count+1)]
    else:
        count_array = [i for i in range(1, count+2)]
    if count <= 1:
        count_array = [i for i in range(1, count+2)]
    form = Contactform(request.POST or None)
    if form.is_valid():
        form.save()
        if next_location:
            return redirect(next)
        return redirect('/index/')
    context = {
        'form': form,
        'articles': article_set,
        'article_query': count_array,
        'category': 'category',
        'index': slug,
        'trending': trending

    }
    return render(request, 'index.html', context)


def article_detail(request, slug):
    # name = requested.POST.get('username')
    hide_value = 'yes'
    main_article = Article.objects.get(slug=slug)
    comments = main_article.comments.all()
    comments = comments.order_by('time_published').reverse()
    if comments.count() > 8:
        comments = comments[:8]
    latest = Article.objects.order_by('date').reverse()[:5]
    trending = Article.objects.order_by('views').reverse()[:5]
    main_article.views += 1
    main_article.save()
    next_location = request.POST.get('next')
    form = CommentForm(request.POST or None)
    count = main_article.comments.count()
    if form.is_valid():
        new_task = form.save()
        main_article.comments.add(new_task)
        date_time = main_article.comments.last().time_published.strftime('%B %d, %Y, %H:%M %p')
        if next_location:
            return redirect(next)
        return JsonResponse({'comments': model_to_dict(new_task), 'date_time': date_time}, status=200)
        detail_page = 'articles/' + slug
        return redirect(detail_page)
    context = {
        'form': form,
        'article': main_article,
        'hide': hide_value,
        'comments': comments,
        'trending': trending,
        'latest': latest,

    }
    return render(request, 'articles/article-detail.html', context)


def get_comments(request, slug, slug2):
    comment_set = Article.objects.get(slug=slug)
    comment_set = comment_set.comments.all()
    int_value = (int(slug2) * 3)
    first_value = ((int(slug2) - 1) * 3)
    count = math.floor(comment_set.count() / 3)
    count_array = [i for i in range(1, comment_set.count() + 1)]
    if int_value > comment_set.count():
        int_value -= comment_set.count()
        article_query = comment_set[:comment_set.count()-first_value][::-1]
        dates = [i.time_published.strftime('%B %d, %Y, %H:%M %p') for i in article_query]

    else:
        article_query = comment_set[first_value - 1:int_value - 1][::-1]
        dates = [i.time_published.strftime('%B %d, %Y, %H:%M %p') for i in article_query]

    return JsonResponse({'article_set': [model_to_dict(i) for i in article_query], 'dates': dates})

# def article_detail(request, slug):
#     main_article = Article.objects.get(slug=slug)
#     if request.method == 'POST':
#         form_valid = Contactform(request.POST)
#         if form_valid.is_valid():
#             name = request.POST.get('username')
#             email = request.POST.get('email')
#             message = request.POST.get('message')
#             contact_app = Contact()
#             contact_app.Fullname = name
#             contact_app.email = email
#             contact_app.message = message
#             contact_app.save()
#             return redirect('detail')
#         else:
#             return render(request, 'articles/article-detail.html', {'article': main_article},)
#
#     else:
#         return render(request, 'articles/article-detail.html', {'article': main_article,'contact': Contactform})





