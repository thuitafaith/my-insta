from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    url(r'^$',views.intro,name = 'intro'),
    url(r'^profile/',views.profile, name = 'profile'),
    url(r'^profile_info/$', views.profile_info, name='owner_profile'),
    url(r'^post/', views.post, name = 'post'),
    url(r'^likes/(?P<image_id>\d+)/$', views.likes, name = 'likes'),
    url(r'^comment/(?P<image_id>\d+)/$', views.comments, name = 'comments')
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
