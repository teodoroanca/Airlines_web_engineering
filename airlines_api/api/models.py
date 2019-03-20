from django.db import models

__all__ = (
    'Time',
    'NumberOfDelays',
    'Flights',
    'MinutesDelayed',
    'Statistics',
    'Entry',
    'Carrier',
    'Airport',
    'DescriptiveStatistics',
    'CarrierReview',
    'CarrierRating'
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
    flights = models.OneToOneField(Flights,
                                   related_name="flights_statistics",
                                   on_delete=models.CASCADE)
    number_of_delays = models.OneToOneField(NumberOfDelays,
                                            related_name="number_of_delays_statistics",
                                            on_delete=models.CASCADE)
    minutes_delayed = models.OneToOneField(
                            MinutesDelayed,
                            related_name="minutes_delayed_statistics",
                            on_delete=models.CASCADE)


class Carrier(models.Model):
    code = models.CharField(blank=False, max_length=10)
    name = models.TextField(blank=False)


class Airport(models.Model):
    code = models.CharField(blank=False, max_length=10)
    name = models.TextField(blank=False)


class Entry(models.Model):
    statistics = models.OneToOneField(Statistics, related_name='statistics_entry', on_delete=models.CASCADE)
    time = models.OneToOneField(Time, related_name='statistics_time', on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, related_name='carrier_entries', on_delete=models.CASCADE)
    airport = models.ForeignKey(Airport, related_name='airport_entries', on_delete=models.CASCADE)


class DescriptiveStatistics(models.Model):
    mean = models.FloatField()
    median = models.FloatField()
    standard_deviation = models.FloatField()
    carrier = models.ForeignKey(Carrier, related_name='carrier_descriptive_statistics', on_delete=models.CASCADE)


class CarrierRating(models.Model):
    carrier = models.ForeignKey(Carrier, related_name='carrier_rating', on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    @property
    def rating(self):
        return float(self.total)/self.votes


class CarrierReview(models.Model):
    carrier = models.ForeignKey(Carrier, related_name='carrier_review', on_delete=models.CASCADE)
    text = models.TextField()



