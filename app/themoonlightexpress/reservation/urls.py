from django.conf.urls import url
from django.contrib.auth import views as auth_view
from . import views

from django.http import HttpResponse, HttpResponseRedirect


urlpatterns = [
    url(r'^$', views.TrainLookUpView, name='reservation'),
    url(r'completereservation',views.reserve,name='reservation'),
    url(r'getreservation',views.search_resersation,name='searchreservation'),
    url(r'expresstrains',views.expressReservationViewSet,name='express schedule'),
    url(r'cancel',views.deletereservation,name='cancel'),
    url(r'rebook',views.rebook,name='rebook')
]