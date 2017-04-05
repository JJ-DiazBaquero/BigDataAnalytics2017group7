from django.conf.urls import url

from . import views
from .views import UsersList, UsersListJson, UsersList110, UsersList110Json, OrderListJson

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^spider', views.spider, name='spider'),
    url(r'^rssfeeds', views.rssfeeds_empty, name='rssfeeds_empty'),
    url(r'^rssfeeds/', views.rssfeeds, name='rssfeeds'),
    url(r'^taller2/', views.taller2, name='taller2'),

    url(r'^datatables_19$', UsersList.as_view(), name="datatables_19"),
    url(r'^users_data_19/$', UsersListJson.as_view(), name="users_list_json_19"),

    url(r'^datatables_110$', UsersList110.as_view(), name="datatables_110"),
    url(r'^users_data_110/$', UsersList110Json.as_view(), name="users_list_json_110"),
    url(r'^ejemplo$', OrderListJson.as_view(), name='order_list_json'),
]