from django.db.models import Q
from rest_framework import serializers
from api.models import (
    Airport,
    Carrier,
    Statistics,
    NumberOfDelays,
    Flights,
    MinutesDelayed,
    Time,
    DescriptiveStatistics,
    CarrierReview,
    CarrierRating
)


class AirportSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Airport
        fields = (
            'code',
            'name',
        )


class CarrierSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Carrier
        fields = (
            'code',
            'name',
        )


class NumberOfDelaysSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = NumberOfDelays
        fields = (
            'late_aircraft',
            'weather',
            'security',
            'national_aviation_system',
            'carrier'
        )


class FlightsSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Flights
        fields = (
            'cancelled',
            'on_time',
            'total',
            'delayed',
            'diverted'
        )


class MinutesDelayedSerializer(serializers.ModelSerializer):

    time = serializers.SerializerMethodField()
    airport = serializers.SerializerMethodField()

    class Meta(object):
        model = MinutesDelayed
        fields = (
            'late_aircraft',
            'weather',
            'carrier',
            'security',
            'total',
            'national_aviation_system',
            'airport',
            'time'
        )

    def get_time(self, obj):
        return obj.minutes_delayed_statistics.statistics_entry.time.label

    def get_airport(self, obj):
        return obj.minutes_delayed_statistics.statistics_entry.airport.code


class StatisticsSerializer(serializers.ModelSerializer):
    number_of_delays = NumberOfDelaysSerializer(many=False)
    flights = FlightsSerializer(many=False)
    minutes_delayed = MinutesDelayedSerializer(many=False)
    time = serializers.SerializerMethodField()

    class Meta(object):
        model = Statistics
        fields = (
            'flights',
            'number_of_delays',
            'minutes_delayed',
            'time'
        )

    def get_time(self, obj):
        time = Time.objects.filter(statistics_time__statistics=obj).first()
        if time:
            return time.label


class SpecificFlightsNumbersSerializer(serializers.ModelSerializer):
    "for point 5"

    class Meta(object):
        model = Flights
        fields = (
            'cancelled',
            'on_time',
            'delayed'
        )


class MinutesDelayedCarrierSpecificSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()
    airport = serializers.SerializerMethodField()

    class Meta(object):
        model = MinutesDelayed
        fields = (
            'late_aircraft',
            'carrier',
            'time',
            'airport'
        )

    def get_time(self, obj):
        return obj.minutes_delayed_statistics.statistics_entry.time.label

    def get_airport(self, obj):
        return obj.minutes_delayed_statistics.statistics_entry.airport.code


# for point 7
class DescriptiveStatisticsSerializer(serializers.ModelSerializer):
    carrier = serializers.SerializerMethodField()

    class Meta(object):
        model = DescriptiveStatistics
        fields = (
            'mean',
            'median',
            'standard_deviation',
            'carrier'
        )

    def get_carrier(self, obj):
        return obj.carrier.code


class CarrierReviewSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = CarrierReview
        fields = (
            'text',
        )


class CarrierRatingSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta(object):
        model = CarrierRating
        fields = (
            'rating',
            'votes'

        )

    def get_rating(self, obj):
        return obj.rating




















