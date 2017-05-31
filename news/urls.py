from django.conf.urls import url
from django.contrib import admin
from news import views
from Zh_news import settings

urlpatterns = [
    url(r'^', views.IndexViews.as_view(), {'document_root': settings.MEDIA_ROOT}, name="index")
]