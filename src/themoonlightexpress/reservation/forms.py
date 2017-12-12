from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class ReservationsForms(forms.Form):
    # here we will get the option  for the resercation
    station_station = forms.ModelChoiceField(queryset=Stations.objects.all())
    end_station = forms.ModelChoiceField(queryset=Stations.objects.all())
    date = forms.DateField(help_text="enter date")

