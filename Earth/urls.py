from django.conf.urls import url
from Earth import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^list/$', views.blog_list, name='list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='detail'),
    url(r'^post/new/$', views.blog_new, name='new'),
    url(r'^admin/$', views.blog_admin, name='admin'),
    url(r'^category/$', views.blog_category, name='category_old'),
    url(r'^category/(.+)/$', views.category, name='category'),
    url(r'^category/(?P<pk>[0-9]+)/del/$', views.blog_category_del, name='category_del'),
    url(r'^tags/(.+)/$', views.tags, name='tags'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.blog_edit, name='edit'),
    url(r'^drafts/$', views.blog_drafts, name='drafts'),
    url(r'^post/(?P<pk>[0-9]+)/publish/$', views.blog_publish, name='publish'),
    url(r'^post/(?P<pk>[0-9]+)/remove/$', views.blog_remove, name='remove'),
    url(r'^posts/archive/(?P<y>[0-9]{4})/(?P<m>[0-9]{1,2})$', views.archives, name='list_by_ym'),
    url(r'^posts/category/(?P<cg>\w+)$', views.post_list_by_category, name='list_by_cg'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact/edit/$', views.contact_edit, name='contact_edit'),
    url(r'^about/$', views.about, name='about'),

    # url(r'^tag(?P<tag>\w+)/$',views.search_tag,name='search_tag'),
]
