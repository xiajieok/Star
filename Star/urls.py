"""Star URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from Earth import views as views
from django.contrib.auth import views as user_views
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from Earth.models import Article
from Earth import models


info_dict = {
    'queryset': models.Article.objects.all(),
    'date_field': 'published_date',
}



urlpatterns = [

    url(r'^$', views.index),
    url(r'^list/$', views.blog_list, name='list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='detail'),
    url(r'^post/new/$', views.blog_new, name='new'),
    url(r'^bs$', views.blog_admin, name='bs'),
    url(r'^bs/category/$', views.admin_category, name='admin_category'),
    url(r'^category/$', views.admin_category, name='category_old'),
    url(r'^category/(.+)/$', views.category, name='category'),
    url(r'^category/(?P<pk>[0-9]+)/del/$', views.blog_category_del, name='category_del'),
    url(r'^tags/(.+)/$', views.tags, name='tags'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.blog_edit, name='edit'),
    url(r'^drafts/$', views.blog_drafts, name='drafts'),
    url(r'^post/(?P<pk>[0-9]+)/publish/$', views.blog_publish, name='publish'),
    url(r'^post/(?P<pk>[0-9]+)/remove/$', views.blog_remove, name='remove'),
    # url(r'^posts/archive/(?P<y>[0-9]{4})/(?P<m>[0-9]{1,2})$', views.archives, name='list_by_ym'),
    url(r'^posts/category/(?P<cg>\w+)$', views.post_list_by_category, name='list_by_cg'),
    # url(r'^contact/$', views.contact, name='contact'),
    # url(r'^contact/edit/$', views.contact_edit, name='contact_edit'),
    url(r'^about/$', views.about, name='about'),
    url(r'^side/$', views.side, name='side'),
    url(r'^edit/$', views.edit, name='edit'),

    url(r'^login/', views.acc_login, name='login'),
    url(r'^logout/', views.acc_logout, name='logout'),
    url(r'^robot/', views.robot, name='robot'),
    url(r'^search/', include('haystack.urls')),

    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'Earth': GenericSitemap(info_dict, priority=0.6)}},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^admin/', admin.site.urls),
    # url(r'^archives/$', Earth.archives, name='archives'),

    # url(r'^accounts/login/$', user_views.login),
    # url(r'^accounts/logout/$', user_views.logout, {'next_page': '/blog'})
]
