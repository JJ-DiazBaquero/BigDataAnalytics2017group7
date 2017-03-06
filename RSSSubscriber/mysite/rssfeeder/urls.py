from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^spider', views.spider, name='spider'),
    url(r'^rssfeeds', views.rssfeeds_empty, name='rssfeeds_empty'),
    url(r'^rssfeeds/', views.rssfeeds, name='rssfeeds'),
]