from django import forms
from crispy_forms.helper import FormHelper
from .models import *


class ReservationsForms(forms.Form):
    # here we will get the option for the resercation
    station_station = forms.ModelChoiceField(queryset=Stations.objects.all())
    end_station = forms.ModelChoiceField(queryset=Stations.objects.all())
    date = forms.DateField(help_text="enter date")

