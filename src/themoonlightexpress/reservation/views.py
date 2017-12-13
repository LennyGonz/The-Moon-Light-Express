from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *

from django.db import connection

# Create your views here.
def Look_up_trains(request):

    if request.method == 'POST':
        cursor = connection.cursor()
        print(">>>>>>>>",getstaion('Boston, MA - South Station', 'Stamford, CT',cursor))

        form = ReservationsForms(request.POST)
        print(form)
        if form.is_valid():
            return HttpResponse("Trains available")
    else:
        form = ReservationsForms()
        return render(request, 'reservation.html', {'form': form})


def getstaion(location, destination,cursor):
    # get train_id, segment_id
    cursor.execute("""select station_id from stations where station_name= %s""", [location])
    startid = cursor.fetchone()
    cursor.execute("""select station_symbol from stations where station_name=%s""", [location])
    startsymbol = cursor.fetchone()
    cursor.execute("""select station_id from stations where station_name=%s""", [destination])
    endid = cursor.fetchone()
    cursor.execute("""select station_symbol from stations where station_name=%s""", [destination])
    endsymbol = cursor.fetchone()
    start_values = []
    end_values = []
    for row in startid, startsymbol:
        start_values.append(row[0])
        # start_values.insert(1,row[0])
    for row in endid, endsymbol:
        end_values.append(row[0])

    print(start_values, end_values)
    return start_values, end_values


def direction(startId, endId):
    if (startId < endId):
        return 1
    else:
        return 0
