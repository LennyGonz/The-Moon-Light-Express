from django import forms
from crispy_forms.helper import FormHelper
from .models import *


class ReservationsForms(forms.Form):
<<<<<<< HEAD
    # here we will get the option for the resercation
    station_station = forms.ModelChoiceField(queryset=Stations.objects.all())
=======
    # here we will get the option  for the resercation
    start_station = forms.ModelChoiceField(queryset=Stations.objects.all())
>>>>>>> 12ef6bf484e8df9e3915c60218df1c39b7311e83
    end_station = forms.ModelChoiceField(queryset=Stations.objects.all())
    date = forms.DateField(help_text="year-month-day: examaple 2017-12-12")


class PassengerForms(forms.Form):
    # here we need to get all the information for the passenger
    fname = forms.CharField(required=True, max_length=30, help_text="Required")
    lname = forms.CharField(required=True, max_length=30, help_text="Required")
    preferred_card_number = forms.CharField(required=True, max_length=30, help_text="Required")
    preferred_billing_address = forms.CharField(required=True, max_length=30, help_text="Required")
    seat_time = forms.CharField(help_text="Child-Adult")