from django.contrib import admin
from django.contrib.admin import ModelAdmin

from api.models import (
    Time,
    NumberOfDelays,
    Flights,
    MinutesDelayed,
    Statistics,
    Entry,
    Carrier,
    Airport
)


@admin.register(Time)
class TimeAdmin(ModelAdmin):
    pass


@admin.register(NumberOfDelays)
class NumberOfDelaysAdmin(ModelAdmin):
    pass


@admin.register(Flights)
class FlightsAdmin(ModelAdmin):
    pass


@admin.register(MinutesDelayed)
class MinutesDelayedAdmin(ModelAdmin):
    pass


@admin.register(Statistics)
class StatisticsAdmin(ModelAdmin):
    pass


@admin.register(Entry)
class EntryAdmin(ModelAdmin):
    pass


@admin.register(Carrier)
class CarrierAdmin(ModelAdmin):
    list_display = ['code']


@admin.register(Airport)
class AirportAdmin(ModelAdmin):
    list_display = ['code']
