"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')

Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from newblog.articles import views as about_views
from newblog.accounts import views as account_views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib.auth import views


article_patterns = [
    url(r'^get_comm/(?P<slug>[\w-]+)/(?P<slug2>[\w-]+)/$', about_views.get_comments, name='get_comments'),
    url(r'^get_comm/(?P<slug>[\w-]+)/$', about_views.get_comments, name='comment_dummy'),
    url(r'^(?P<slug>[\w-]+)/$', about_views.article_detail, name='detail'),
    url(r'^category/(?P<slug>[\w-]+)/$', about_views.by_category, name='category'),
    url(r'^category/(?P<slug>[\w-]+)/(?P<slug2>[\w-]+)/$', about_views.category2, name='category2'),
]


urlpatterns = [
    url(r'^index/(?P<slug>[\w-]+)/$', about_views.index2, name='index2'),
    path('index/', about_views.index, name='index'),
    path(r'admin/', admin.site.urls),
    url(r'^articles/', include(article_patterns)),


]


urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

