from django.db.models import Q
from rest_framework import serializers
from api.models import (
    Airport,
    Carrier,
    CarrierRating,
    CarrierReview,
    DescriptiveStatistics,
    Flights,
    MinutesDelayed,
    NumberOfDelays,
    Statistics,
    Time,
)


class AirportSerializer(serializers.ModelSerializer):
    """
    Airport serializer
    Will retrieve:
        -Code
        -Name
        -Link for operating carriers at this airport
    """
    link_operating_carriers = serializers.SerializerMethodField()

    class Meta(object):
        model = Airport
        fields = (
            'code',
            'name',
            'link_operating_carriers',
        )

    def get_link_operating_carriers(self, obj):
        return "api/airports/"+obj.code+"/carriers/"


class CarrierSerializer(serializers.ModelSerializer):
    """
    Carrier serializer
    Will retrieve:
        -Code
        -Name
        -Link for statistics of this carrier
        -Link for reviews of this carrier
        -Link for ratings of this carrier
    """
    link_statistics = serializers.SerializerMethodField()
    link_reviews = serializers.SerializerMethodField()
    link_ratings = serializers.SerializerMethodField()

    class Meta(object):
        model = Carrier
        fields = (
            'code',
            'name',
            'link_statistics',
            'link_reviews',
            'link_ratings',
        )

    def get_link_statistics(self, obj):
        return "api/airports/"+obj.code+"/statistics/"

    def get_link_reviews(self, obj):
        return "api/airports/"+obj.code+"/reviews/"

    def get_link_ratings(self, obj):
        return "api/airports/"+obj.code+"/ratings/"


class NumberOfDelaysSerializer(serializers.ModelSerializer):
    """
    Serializer for number of delays
    Will retrieve how many delays were due to:
        -Late aircraft
        -Weather
        -Security
        -National aviation system
        -Carrier
    """
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
    """
    Serializer for number of flights
    Will retrieve how many flights were:
        -Cancelled
        -On time
        -In total
        -Delayed
        -Diverted
    """
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
    """
    Serializer for number of delayed minutes due to
    Will retrieve how many flights were:
        -Late aircraft
        -Weather
        -Carrier
        -In total
        -National aviation system
        -Airport
        -Timestamp of the statistic
    """
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
    """
    Serializer for statistics of a given airport for a given carrier in a given month
    Will retrieve:
        -Number of delays (Serializer)
        -Flights (Serializer)
        -Minutes Delayed (Serializer)
        -Timestamp
        -Link for number of delays route (Serializer)
        -Link for minutes delayed route (Serializer)
        -Link for deletion of the entry
    """
    number_of_delays = NumberOfDelaysSerializer(many=False)
    flights = FlightsSerializer(many=False)
    minutes_delayed = MinutesDelayedSerializer(many=False)
    time = serializers.SerializerMethodField()

    link_flights = serializers.SerializerMethodField()
    link_number_of_delays = serializers.SerializerMethodField()
    link_minutes_delayed = serializers.SerializerMethodField()
    link_delete = serializers.SerializerMethodField()

    class Meta(object):
        model = Statistics
        fields = (
            'flights',
            'number_of_delays',
            'minutes_delayed',
            'time',
            'link_flights',
            'link_number_of_delays',
            'link_minutes_delayed',
            'link_delete'
        )

    def get_time(self, obj):
        time = Time.objects.filter(statistics_time__statistics=obj).first()
        if time:
            return time.label

    def get_link_flights(self, obj):
        return "api/airports/"+obj.statistics_entry.airport.code+"/carriers/" + \
               obj.statistics_entry.carrier.code+"/statistics/"+"flights"

    def get_link_number_of_delays(self, obj):
        return "api/airports/"+obj.statistics_entry.airport.code+"/carriers/" + \
               obj.statistics_entry.carrier.code+"/statistics/"+"number-of-delays"

    def get_link_minutes_delayed(self, obj):
        return "api/airports/"+obj.statistics_entry.airport.code+"/carriers/" + \
               obj.statistics_entry.carrier.code+"/statistics/"+"minutes-delayed"

    def get_link_delete(self, obj):
        return "api/airports/"+obj.statistics_entry.airport.code+"/carriers/" + \
               obj.statistics_entry.carrier.code+"/statistics/"+"delete"


class SpecificFlightsNumbersSerializer(serializers.ModelSerializer):
    """
    Serializer for specific flights numbers (cancelled, on_time, delayed)
    of a given airport for a given carrier in a given month
    """

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


class DescriptiveStatisticsSerializer(serializers.ModelSerializer):
    """
        Serializer for mean, media, standard deviation of a carrier
    """
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
    """
        Serializer for reviews of a carrier
    """
    class Meta(object):
        model = CarrierReview
        fields = (
            'text',
        )


class CarrierRatingSerializer(serializers.ModelSerializer):
    """
        Serializer for ratings of a carrier
    """
    rating = serializers.SerializerMethodField()

    class Meta(object):
        model = CarrierRating
        fields = (
            'rating',
            'votes'

        )

    def get_rating(self, obj):
        return obj.rating

