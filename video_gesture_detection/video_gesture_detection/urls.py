"""video_gesture_detection URL Configuration

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
from gesture import views as gesture_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', gesture_views.home, name='home'),
    url(r'^video_gesture_pre/$', gesture_views.video_gesture_pre, name='video_gesture_pre'),
    url(r'^video_gesture_pre_no_outline/$', gesture_views.video_gesture_pre_no_outline, name='video_gesture_pre_no_outline'),
    url(r'^video_gesture_pre_all/$', gesture_views.video_gesture_pre_all, name='video_gesture_pre_all'),
    url(r'^video_gesture_pre_all_no_outline/$', gesture_views.video_gesture_pre_all_no_outline, name='video_gesture_pre_all_no_outline'),
    url(r'^get_emotion_data/$', gesture_views.video_gesture_pre, name='get_emotion_data'),
    url(r'^get_attention_data/$', gesture_views.video_gesture_pre, name='get_attention_data'),
    url(r'^yawn_detection/$', gesture_views.yawn_detection, name='yawn_detection'),
    url(r'^video_gesture_pre1', gesture_views.video_gesture_pre1, name='video_gesture_pre1'),
]
