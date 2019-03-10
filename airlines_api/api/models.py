from django.db import models

__all__ = (
    'Time',
    'NumberOfDelays',
    'Flights',
    'MinutesDelayed',
    'Statistics',
    'Entry',
    'Carrier',
    'Airport'
)


class Time(models.Model):
    month = models.IntegerField(blank=False)
    year = models.IntegerField(blank=False)
    label = models.CharField(blank=False, max_length=10)


class NumberOfDelays(models.Model):
    carrier = models.IntegerField(blank=False)
    late_aircraft = models.IntegerField(blank=False)
    national_aviation_system = models.IntegerField(blank=False)
    security = models.IntegerField(blank=False)
    weather = models.IntegerField(blank=False)


class Flights(models.Model):
    cancelled = models.IntegerField(blank=False)
    delayed = models.IntegerField(blank=False)
    diverted = models.IntegerField(blank=False)
    on_time = models.IntegerField(blank=False)
    total = models.IntegerField(blank=False)


class MinutesDelayed(models.Model):
    carrier = models.IntegerField(blank=False)
    late_aircraft = models.IntegerField(blank=False)
    national_aviation_system = models.IntegerField(blank=False)
    security = models.IntegerField(blank=False)
    total = models.IntegerField(blank=False)
    weather = models.IntegerField(blank=False)


class Statistics(models.Model):
    number_of_delays = models.OneToOneField(NumberOfDelays, on_delete=models.CASCADE)
    flights = models.OneToOneField(Flights, on_delete=models.CASCADE)
    minutes_delayed = models.OneToOneField(MinutesDelayed, on_delete=models.CASCADE)


class Carrier(models.Model):
    code = models.CharField(blank=False, max_length=10)
    name = models.TextField(blank=False)


class Airport(models.Model):
    code = models.CharField(blank=False, max_length=10)
    name = models.TextField(blank=False)


class Entry(models.Model):
    statistics = models.OneToOneField(Statistics, on_delete=models.CASCADE)
    time = models.OneToOneField(Time, on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)


