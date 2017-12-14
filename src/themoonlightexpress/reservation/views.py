from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .carlos_functions_djago import *


# Create your views here.
# Create your views here.
def TrainLookUpView(request,METHOD=['GET','POST']):
    if request.method == 'POST':
        form = ReservationsForms(request.POST)
        trainslist = None
        if form.is_valid():
            start = request.POST['start_station']
            end = request.POST['end_station']
            train_direction = direction(start, end)
            day = MF(date1=request.POST['date'])
            trainsid = trainsavible(train_direction, day)
            trainslist = trainsid
            # return render(request, "displaytrain.html", resource)
        return render(request,'listrains.html',{"trains":trainslist})
    else:
        form = ReservationsForms()
        return render(request, 'reservation.html', {'form': form})


def PassengerView(request, METHOD=["GET", "POST"]):
    if request.method == 'POST':
        #print(request.POST)
        form = PassengerForms(request.POST)
        if form.is_valid():
            ## here we extract information to save the information
            ## to register this in passenger
            pass
