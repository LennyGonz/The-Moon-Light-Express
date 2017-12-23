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
            print(request.POST['date'])
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
                                                  "date": date,
                                                  "fare_A": fare})
    else:
        form = ReservationsForms()
        return render(request, 'reservation.html', {'form': form})


def reserve(request, METHOD=["GET", "POST"]):
    if request.method == 'POST':
        form = reserveForm(request.POST)
        print(" >> ", request.GET["fare"])
        if form.is_valid():
            passengerInfo = {
                "fname": request.POST['firstname'],
                "lname": request.POST['lastname'],
                "email": request.POST['email'],
                "preferred_card_number": request.POST['preferred_card_number'],
                "preferred_billing_address": request.POST['preferred_card_number']
            }
            Passengers.objects.create(**passengerInfo)
            try:
                _passenger = Passengers.objects.get(email=request.POST['email'])
            except Exception:
                return HttpResponse("our records show this already exits. go back and change email address to proceed")

            reservationInfo = {
                "reservation_date": datetime.datetime.today().strftime('%Y-%m-%d'),
                "paying_passenger": _passenger,
                "card_number": request.POST['preferred_card_number'],
                "billing_address": request.POST['preferred_billing_address']
            }
            Reservations.objects.create(**reservationInfo)

            tripInfo = {
                "trip_date": request.POST['trip_date'],
                "trip_seg_start": Segments.objects.get(seg_n_end__station_name=request.POST['start_station']),
                "trip_seg_ends": Segments.objects.get(seg_s_end__station_name=request.POST['end_station']),
                "fare_type": FareTypes.objects.get(fare_id=request.POST['fare_type']),
                "fare": request.GET["fare"],
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
                "fare": details.fare,
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
        Cancellation(request.GET["reservation"])
        return HttpResponse("Your Trip has been canceled")


def expressReservationViewSet(request, MeTHOD=["GET", "POST"]):
    # express stations 1,7,13,19,25
    if request.method == 'POST':
        form = ExtressReservationForm(request.POST)
        train_and_startime = {}
        trainslist = None
        start_station = None
        end_station = None
        date_ta = None

        print(request.POST['date'])

        if form.is_valid():
            start = request.POST['start_station']
            end = request.POST['end_station']
            _date = request.POST['date']

            # if request.POST['date'] < datetime.datetime.today():
            #     return HttpResponse("This date is Not Valid please Choose a date in the future")
            train_direction = direction(start, end)
            day = MF(date1=request.POST['date'])
            trainsid = trainsavible(train_direction, day)
            fare_type = 'adult'
            print()
            fare, startseg, endseg,trainslist = expressTrain(location=start, destination=end,date=_date, faretype=fare_type)
            print(len(trainslist))
            if len(trainslist) < 1:
                start_station = Stations.objects.get(station_id=start)
                end_station = Stations.objects.get(station_id=end)
                date = request.POST['date']

                return render(request, "noTrainsAvailable.html", {"trains": train_and_startime,
                                                                  "start": start_station,
                                                                  "end": end_station,
                                                                  "date": _date,
                                                                  "fare_A": fare})
            for data in trainslist:
                train_and_startime[data[0]] = data[1]
            start_station = Stations.objects.get(station_id=start)
            end_station = Stations.objects.get(station_id=end)
            date = request.POST['date']

        return render(request, 'listrains.html', {"trains": train_and_startime,
                                                  "start": start_station,
                                                  "end": end_station,
                                                  "date": date,
                                                  "fare_A": fare})
    else:
        form = ExtressReservationForm()
        return render(request, "expressreservationform.html", {"form": form})
