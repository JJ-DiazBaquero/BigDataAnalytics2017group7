from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^taller1/', include('rssfeeder.urls')),
    url(r'^admin/', admin.site.urls),
]