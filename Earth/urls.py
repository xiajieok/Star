from django.conf.urls import patterns, include, url
from Earth import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^list/$', views.blog_list,name='list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='detail'),
    url(r'^post/new/$', views.blog_new, name='new'),
    url(r'^admin/$', views.blog_admin, name='admin'),
    url(r'^category/$', views.blog_category, name='category'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.blog_edit, name='edit'),
    url(r'^drafts/$', views.blog_drafts, name='drafts'),
    url(r'^post/(?P<pk>[0-9]+)/publish/$', views.blog_publish, name='publish'),
    url(r'^post/(?P<pk>[0-9]+)/remove/$', views.blog_remove, name='remove'),
    url(r'^posts/archive/(?P<y>[0-9]{4})/(?P<m>[0-9]{1,2})$', views.archives, name='list_by_ym'),
    # url(r'^tag(?P<tag>\w+)/$',views.search_tag,name='search_tag'),
]
