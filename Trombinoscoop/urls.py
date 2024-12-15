"""Trombinoscoop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import re_path as url
from django.contrib import admin
from Trombinoscoop.views import welcome,login,register
from Trombinoscoop.views import logout
from Trombinoscoop.views import add_friend, delete_friend_request
from Trombinoscoop.views import show_profile, modify_profile
from Trombinoscoop.views import ajax_check_email_field
urlpatterns = [
    #   name = 'login'  consite a appeler les liens dans page.html dans les form avec l'attribut action = 'login'
    # url('pour appele dans les liens ', fonction, pour appler dans  )
    url(r'^$', welcome),
    url(r'^login/$', login, name= 'login'),
    url(r'^welcome$', welcome , name= 'welcome'),
    url(r'^register/$', register, name = 'register'),
    url(r'^addFriend$', add_friend, name = 'addFriend'),
    url(r'^showProfile$', show_profile),
    url(r'^modifyProfile$', modify_profile, name='modifyprofile'),
    url(r'^delete_friend_request/(?P<id>\d+)/$', delete_friend_request, name='delete_friend_request'),
    url(r'^logout$', logout , name='logout' ),
    url(r'^ajax/checkEmailField$', ajax_check_email_field),
    url(r'^admin/', admin.site.urls),
]
