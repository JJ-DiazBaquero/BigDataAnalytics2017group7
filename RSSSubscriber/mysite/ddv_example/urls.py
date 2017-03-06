from django.conf.urls import url

from .views import UsersList, UsersListJson, IndexView, UsersList110, UsersList110Json, OrderListJson


urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^datatables_19$', UsersList.as_view(), name="datatables_19"),
    url(r'^users_data_19/$', UsersListJson.as_view(), name="users_list_json_19"),

    url(r'^datatables_110$', UsersList110.as_view(), name="datatables_110"),
    url(r'^users_data_110/$', UsersList110Json.as_view(), name="users_list_json_110"),
    url(r'^ejemplo$', OrderListJson.as_view(), name='order_list_json'),
]