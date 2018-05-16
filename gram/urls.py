from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    url(r'^$',views.intro,name = 'intro'),
    url(r'^profile/',views.profile, name = 'profile'),
    url(r'^post/', views.post, name = 'post'),
    url(r'^likes/(?P<image_id>)/$', views.likes, name = 'likes')
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
