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
from Earth import views as Earth
from django.contrib.auth import views as user_views

urlpatterns = [

    url(r'^$', Earth.index),
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('Earth.urls')),
    url(r'^cmdb/', include('Moon.urls')),
    url(r'^login/', Earth.acc_login, name='login'),
    url(r'^logout/', Earth.acc_logout, name='logout'),
    # url(r'^archives/$', Earth.archives, name='archives'),

    # url(r'^accounts/login/$', user_views.login),
    # url(r'^accounts/logout/$', user_views.logout, {'next_page': '/blog'})
]
