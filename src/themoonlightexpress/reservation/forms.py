from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class ReservationsForms(forms.Form):
    # here we will get the option  for the resercation
    station_station = forms.ModelChoiceField(queryset=Stations.objects.all())
    end_station = forms.ModelChoiceField(queryset=Stations.objects.all())
    date = forms.DateField(help_text="month-day-year")


class PassengerForms(forms.Form):
    # here we need to get all the information for the passenger
    fname = forms.CharField(required=True, max_length=30, help_text="Required")
    lname = forms.CharField(required=True, max_length=30, help_text="Required")
    preferred_card_number = forms.CharField(required=True, max_length=30, help_text="Required")
    preferred_billing_address = forms.CharField(required=True, max_length=30, help_text="Required")
    seat_time = forms.CharField(help_text="Child-Adult")