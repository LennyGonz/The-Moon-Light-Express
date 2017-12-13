from django.conf.urls import url
from django.contrib.auth import views as auth_view
from . import views

from django.http import HttpResponse, HttpResponseRedirect


urlpatterns = [
    url(r'^reservation/$', views.reservations, name='reservation'),

]