from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .carlos_functions_djago import *


# Create your views here.
# Create your views here.
def TrainLookUpView(request, METHOD=['GET', 'POST']):
    if request.method == 'POST':
        form = ReservationsForms(request.POST)
        train_and_startime = {}
        train_and_endtime = {}
        trainslist = None
        if form.is_valid():
            start = request.POST['start_station']
            end = request.POST['end_station']
            train_direction = direction(start, end)
            day = MF(date1=request.POST['date'])
            trainsid = trainsavible(train_direction, day)
            fake_fare_type = 'adult'
            fare,startseg,endseg,trainslist = ChoosingTrain(location=start,destination=end,
                                                            date=request.POST['date'],faretype=fake_fare_type)
            for data in trainslist:
                train_and_startime[data[0]] = data[1]

        return render(request, 'listrains.html', {"trains": train_and_startime})
    else:
        form = ReservationsForms()
        return render(request, 'reservation.html', {'form': form})


def reserve(request, METHOD=["GET", "POST"]):
    if request.method == 'POST':
        form = reserveForm(request.POST)
        print(request.POST)
        if form.is_valid():
            pass
        return HttpResponse("This is your Trip")

    else:
        form = reserveForm(request.GET)
        return render(request,"complete.html",{"form":form})
