"""untitled4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.conf.urls import url

from Text import views

urlpatterns = [
    url(r'^hello$', views.hello),
    url(r'^testdb$', views.testdb),
    url(r'^admin/', admin.site.urls),
    url(r'^upLoad$', views.upLoadFile),
    url(r'^music$', views.musicCr),
    url(r'^house/album$',views.houseMusicAlbum),
    url(r'^house/album/detail$', views.musicAlbumDetail),
    url(r'^downLoadFile/(?P<file_name>.*)/$', views.downLoadFile),
    url(r'^artist$', views.artistList),
    url(r'^country$', views.country),
    url(r'^sound$', views.sound),
    url(r'^user/collect/up$', views.userCollectUp),
    url(r'^user$', views.userAdd),
    url(r'^version', views.version),

]
