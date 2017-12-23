# from django.contrib import admin
#
# # Register your models here.
#
# from .models import *
# from django.contrib import admin
#
#
# class FareTypesAdmin(admin.ModelAdmin):
#     list_display = ["fare_id", "fare_name", "rate"]
#
#
# admin.site.register(FareTypes, FareTypesAdmin)
#
#
# class PassengersAdmin(admin.ModelAdmin):
#     list_display = ["passenger_id", "fname", "lname", "email", "preferred_billing_address"]
#
#
# admin.site.register(Passengers, PassengersAdmin)
#
#
# class ReservationsAdmin(admin.ModelAdmin):
#     list_display = ["reservation_id", "reservation_date", "paying_passenger", "card_number", "billing_address"]
#
#
# admin.site.register(Reservations, ReservationsAdmin)
#
#
# class SeatsFreeAdmin(admin.ModelAdmin):
#     list_display = ["train", "segment", "seat_free_date", "freeseat"]
#
#
# admin.site.register(SeatsFree, SeatsFreeAdmin)
#
#
# class SegmentsAdmin(admin.ModelAdmin):
#     list_display = ["segment_id", "seg_n_end", "seg_s_end", "seg_fare"]
#
#
# admin.site.register(Segments, SegmentsAdmin)
#
#
# class StationAdmin(admin.ModelAdmin):
#     list_display = ["station_id", "station_name", "station_symbol"]
#
#
# admin.site.register(Stations, StationAdmin)
#
#
# class StopsAtAdmin(admin.ModelAdmin):
#     list_display = ["train", "station", "time_in", "time_out"]
#
#
# admin.site.register(StopsAt, StopsAtAdmin)
#
#
# class TrainsAdmin(admin.ModelAdmin):
#     list_display = ["train_id", "train_start", "train_end", "train_direction", "train_days"]
#
#
# admin.site.register(Trains, TrainsAdmin)
#
#
# class TripsAdmin(admin.ModelAdmin):
#     list_display = ["trip_id", "trip_date", "trip_seg_start", "trip_seg_ends", "fare_type", "fare", "trip_train","reservation"]
#
#
# admin.site.register(Trips,TripsAdmin)
