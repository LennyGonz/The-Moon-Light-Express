from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *


# Create your views here.
def reservations(request, methods=["GET","POST"]):
    if request.method == 'POST':
        form = ReservationsForms(request.POST)
        print(form)
        if form.is_valid():
            return HttpResponse("Reservation made")
    else:
        form = ReservationsForms()
        return render(request, 'reservation.html', {'form': form})


