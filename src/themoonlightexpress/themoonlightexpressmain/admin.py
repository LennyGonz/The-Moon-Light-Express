from django.contrib import admin

# Register your models here.

from .models import *
from django.contrib import admin


admin.site.register(FareTypes)
admin.site.register(Passengers)
admin.site.register(Reservations)
admin.site.register(SeatsFree)
admin.site.register(Segments)
admin.site.register(Stations)
admin.site.register(StopsAt)
admin.site.register(Trains)
admin.site.register(Trips)