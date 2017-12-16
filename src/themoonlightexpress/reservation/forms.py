from django import forms
from .models import *


class ReservationsForms(forms.Form):
    # here we will get the option  for the resercation
    start_station = forms.ModelChoiceField(queryset=Stations.objects.all())
    end_station = forms.ModelChoiceField(queryset=Stations.objects.all())
    date = forms.DateField(help_text="year-month-day: examaple 2017-12-12")

class reserveForm(forms.Form):
    # here we need to get all the information for the passenger
    train = forms.IntegerField(required=True,max_value=50, help_text="Train selected")
    departuretime = forms.TimeField()
    arivaltime = forms.TimeField()
    start_station = forms.CharField(required=True,help_text="start station")
    end_station = forms.CharField(required=True,help_text="end station")
    trip_date = forms.DateField(required=True,help_text="Trip Date")

    firstname = forms.CharField(required=True, max_length=30, help_text="First Name")
    lastname = forms.CharField(required=True, max_length=30, help_text="Last Name")
    preferred_card_number = forms.CharField(required=True, max_length=30, help_text="Required")
    preferred_billing_address = forms.CharField(required=True, max_length=30, help_text="Required")
    email = forms.EmailField(required=True,help_text="Required")
    fare_type = forms.ModelChoiceField(queryset=FareTypes.objects.all(),help_text="adult/child/senior")
