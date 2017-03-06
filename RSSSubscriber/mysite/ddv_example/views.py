# -*- coding: utf8 -*-
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from models import Profesor
import backend

class OrderListJson(BaseDatatableView):
# The model we're going to show
    model = Profesor
    columns = ['nombre','departamento', 'cargo', 'curso', 'correo','estudios','extension','sitioWeb','oficina','area','grupoInvestigacion']
    order_columns = ['nombre','departamento', 'cargo', 'curso', 'correo','estudios','extension','sitioWeb','oficina','area','grupoInvestigacion']
    max_display_length = 100
    def render_column(self, row, column):
        if column == 'name':
            return '{0} {1}'.format(row.customer_firstname, row.customer_lastname)
        else:
            return super(OrderListJson, self).render_column(row, column)
    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(name__istartswith=search)

class IndexView(TemplateView):
    template_name = 'ddv_example/index.html'


class UsersList110(TemplateView):
    backend.correrCrawler()
    template_name = 'ddv_example/users_list_1_10.html'


class UsersList110Json(BaseDatatableView):
    model = Profesor
    columns = ['nombre','departamento', 'cargo', 'curso', 'correo','estudios','extension','sitioWeb','oficina','area','grupoInvestigacion']
    order_columns = ['nombre','departamento', 'cargo', 'curso', 'correo','estudios','extension','sitioWeb','oficina','area','grupoInvestigacion']

# backward compatibility with Datatables 1.9.x
class UsersList(TemplateView):
    template_name = 'ddv_example/users_list.html'


class UsersListJson(BaseDatatableView):
    model = Profesor
    columns = ['nombre','departamento', 'cargo', 'curso', 'correo','estudios','extension','sitioWeb','oficina','area','grupoInvestigacion']
    order_columns = ['nombre','departamento', 'cargo', 'curso', 'correo','estudios','extension','sitioWeb','oficina','area','grupoInvestigacion']

    def filter_queryset(self, qs):
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            qs = qs.filter(Q(username__istartswith=sSearch) | Q(email__istartswith=sSearch))
        return qs