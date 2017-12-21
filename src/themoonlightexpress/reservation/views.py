from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .carlos_functions_djago import *
import datetime


# Create your views here.
# Create your views here.
def TrainLookUpView(request, METHOD=['GET', 'POST']):
    if request.method == 'POST':
        form = ReservationsForms(request.POST)
        train_and_startime = {}
        trainslist = None
        start_station = None
        end_station = None
        date = None

        if form.is_valid():
            start = request.POST['start_station']
            end = request.POST['end_station']

            # if request.POST['date'] < datetime.datetime.today():
            #     return HttpResponse("This date is Not Valid please Choose a date in the future")
            train_direction = direction(start, end)
            day = MF(date1=request.POST['date'])
            trainsid = trainsavible(train_direction, day)
            fake_fare_type = 'adult'
            fare, startseg, endseg, trainslist = ChoosingTrain(location=start, destination=end,
                                                               date=request.POST['date'], faretype=fake_fare_type)
            for data in trainslist:
                train_and_startime[data[0]] = data[1]
            start_station = Stations.objects.get(station_id=start)
            end_station = Stations.objects.get(station_id=end)
            date = request.POST['date']

        return render(request, 'listrains.html', {"trains": train_and_startime,
                                                  "start": start_station,
                                                  "end": end_station,
                                                  "date": date})
    else:
        form = ReservationsForms()
        return render(request, 'reservation.html', {'form': form})


def reserve(request, METHOD=["GET", "POST"]):
    if request.method == 'POST':
        form = reserveForm(request.POST)
        print(request.POST)
        if form.is_valid():
            passengerInfo = {
                "fname": request.POST['firstname'],
                "lname": request.POST['lastname'],
                "email": request.POST['email'],
                "preferred_card_number": request.POST['preferred_card_number'],
                "preferred_billing_address": request.POST['preferred_card_number']
            }
            Passengers.objects.create(**passengerInfo)

            reservationInfo = {
                "reservation_date": datetime.datetime.today().strftime('%Y-%m-%d'),
                "paying_passenger": Passengers.objects.get(email=request.POST['email']),
                "card_number": request.POST['preferred_card_number'],
                "billing_address": request.POST['preferred_billing_address']
            }
            Reservations.objects.create(**reservationInfo)

            tripInfo = {
                "trip_date": request.POST['trip_date'],
                "trip_seg_start": Segments.objects.get(seg_n_end__station_name=request.POST['start_station']),
                "trip_seg_ends": Segments.objects.get(seg_s_end__station_name=request.POST['end_station']),
                "fare_type": FareTypes.objects.get(fare_id=request.POST['fare_type']),
                "fare": 90,
                "trip_train": Trains.objects.get(train_id=request.POST['train']),
                "reservation": Reservations.objects.get(paying_passenger__email=request.POST['email'])
            }
            Trips.objects.create(**tripInfo)

            tripInfo["departuretime"] = request.POST['departuretime']
            tripInfo["arivaltime"] = request.POST['arivaltime']

        return render(request, "tripconfirmation.html", {"trip": tripInfo})

    else:
        form = reserveForm(request.GET)
        return render(request, "complete.html", {"form": form})


def search_resersation(request, METHOD=["GET", "POST"]):
    if request.method == "POST":
        form = Search_resersationform(request.POST)
        if form.is_valid():
            __trip = request.POST["reservation_Number"]
            details = Trips.objects.get(reservation=__trip)

            tripInfo = {
                "trip_date": details.trip_date,
                "trip_seg_start": details.trip_seg_start,
                "trip_seg_ends": details.trip_seg_ends,
                "fare_type": details.fare_type,
                "fare": 90,
                "trip_train": details.trip_train,
                "reservation": details.reservation
            }
            start = Stations.objects.get(station_name=details.trip_seg_start).station_id
            end = Stations.objects.get(station_name=details.trip_seg_ends).station_id
            ###### don't touch #########
            list = details.trip_train
            tl = []
            tl.append(list)
            ##### don't touch ##########
            time = get_time(tl, start, end)
            tripInfo["departuretime"] = time[0][0]
            tripInfo["arivaltime"] = time[0][1]

            return render(request, "search.html", {"TripInfo": tripInfo})
    else:
        form = Search_resersationform()
        return render(request, "lookup.html", {"form": form})


def deletereservation(request, METHOD=["GET", "POST"]):
    if request.method == "GET":
        print(request.GET)
        return HttpResponse("Your Trip has been canceled")

