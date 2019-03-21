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
    """
        Each Time objects is defined by:
            -A month
            -A year
        Label is the concatenation of month and year
    """
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
    """
        Each statistics objects has 3 1-to-1 relationships to:
            - A Flights object
            - A NumberOfDelays object
            - A MinutesDelayed object
    """
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
    """
        Each carrier has:
            -A code
            -A name
    """
    code = models.CharField(blank=False, max_length=10)
    name = models.TextField(blank=False)


class Airport(models.Model):
    """
        Each airports has:
            -A code
            -A name
    """
    code = models.CharField(blank=False, max_length=10)
    name = models.TextField(blank=False)


class Entry(models.Model):
    """
    Each entry is defined by:
        -A month and a year
        -A carrier
        -An airport

    It has a statistics object associated
    """
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
    """
        Each object of this type stores:
            - A refference to a Carrier
            - Number of votes
            - Total number of "stars"
    """
    carrier = models.ForeignKey(Carrier, related_name='carrier_rating', on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    @property
    def rating(self):
        """
        Computing the average rating by dividing the sum of stars by the number of votes
        """
        return float(self.total)/self.votes


class CarrierReview(models.Model):
    """
        Each object of this type stores:
            -A text
            -A refference to a Carrier
    """
    carrier = models.ForeignKey(Carrier, related_name='carrier_review', on_delete=models.CASCADE)
    text = models.TextField()



