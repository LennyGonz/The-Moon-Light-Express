from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *


class ReservationsForms(forms.Form):
    # here we will get the option  for the resercation
    start_station = forms.ModelChoiceField(queryset=Stations.objects.all())
    end_station = forms.ModelChoiceField(queryset=Stations.objects.all())
    date = forms.DateField(help_text="year-month-day: examaple 2017-12-12")

class reserveForm(forms.Form):
    # here we need to get all the information for the passenger
    train = forms.IntegerField(required=True,max_value=50)
    departuretime = forms.TimeField()
    arivaltime = forms.TimeField()
    start_station = forms.CharField(required=True,)
    end_station = forms.CharField(required=True,)
    trip_date = forms.DateField(required=True,)

    firstname = forms.CharField(required=True, max_length=30,)
    lastname = forms.CharField(required=True, max_length=30,)
    preferred_card_number = forms.CharField(required=True, max_length=30,)
    preferred_billing_address = forms.CharField(required=True, max_length=30,)
    email = forms.EmailField(required=True,)
    fare_type = forms.ModelChoiceField(queryset=FareTypes.objects.all(),)

class Search_resersationform(forms.Form):
    reservation_Number = forms.IntegerField(help_text="Enter reservation number printed on your reciept")