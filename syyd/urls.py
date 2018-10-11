"""syyd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from book import views as book_views

urlpatterns = [
    url(r'^$', book_views.home, name='home'),

    url(r'^admin/', admin.site.urls),

    # 小说的根目录，除了包含小说的章节目录，还可以包含其他信息，以后再添加
    url(r'^(?P<novel_id>\d+)/$', book_views.dir, name='novel_root'),
    url(r'^(?P<novel_id>\d+)/dir.html/$', book_views.dir, name='novel_dir'),
    url(r'^(?P<novel_id>\d+)/(?P<chapter_num>\d+).html/$', book_views.read_chapter, name='novel_chapter'),

    url(r'search/result.html/$', book_views.search, name='search'),
    url(r'author/(?P<author_id>\d+).html', book_views.author_novels, name='author_novels'),

    url(r'sort/$', book_views.sort, name='sort'),
    url(r'sort/(?P<category>.*).html', book_views.sort_category, name='sort_catogery'),
]
