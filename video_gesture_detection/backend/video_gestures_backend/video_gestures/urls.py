"""video_gestures URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from video_gestures.main_server import views as gesture_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', gesture_views.home, name='home'),
    url(r'^realtime_stats/$', gesture_views.display_realtime_stats, name='display_realtime_stats'),
    url(r'^get_stats/$', gesture_views.get_stats, name='get_stats'),
    url(r'^recommendation_creation/$', gesture_views.recommendation_creation, name='recommendation_creation'),

]
