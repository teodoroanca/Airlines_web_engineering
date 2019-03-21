from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import generics, status
from django.http import Http404, HttpResponse
from django.db.models import Q
from rest_framework.settings import api_settings
from rest_framework_csv import renderers as r

import statistics

from api.models import (
    Airport,
    Carrier,
    CarrierRating,
    CarrierReview,
    DescriptiveStatistics,
    Entry,
    Flights,
    MinutesDelayed,
    NumberOfDelays,
    Statistics,
)

from api.serializers import (
    AirportSerializer,
    CarrierRatingSerializer,
    CarrierReviewSerializer,
    CarrierSerializer,
    DescriptiveStatisticsSerializer,
    FlightsSerializer,
    MinutesDelayedCarrierSpecificSerializer,
    MinutesDelayedSerializer,
    NumberOfDelaysSerializer,
    SpecificFlightsNumbersSerializer,
    StatisticsSerializer,
)


def csv_renderer(self):
    """
    Changing the renders to csv type in case it is requested
    """
    content_type = self.request.GET.get('Content-Type', None)
    if content_type == "text/csv":
        renderers = (r.CSVRenderer,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    else:
        renderers = api_settings.DEFAULT_RENDERER_CLASSES

    return [renderer() for renderer in renderers]


class AirportViewSet(ModelViewSet):
    """
        View for Airports
    """
    model = Airport
    serializer_class = AirportSerializer
    http_method_names = ['get']

    def get_renderers(self):
        return csv_renderer(self)

    def get_queryset(self):
        queryset = Airport.objects.all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        airport_code = self.request.parser_context['kwargs']['pk']
        try:
            instance = Airport.objects.get(code=airport_code)

        except Airport.DoesNotExist:
            raise Http404

        serializer = AirportSerializer(instance)
        return Response(serializer.data)


class CarrierViewSet(ModelViewSet):
    """
        View for carrier
    """
    model = Carrier
    serializer_class = CarrierSerializer
    http_method_names = ['get', 'post']

    def get_renderers(self):
        return csv_renderer(self)

    def get_queryset(self):
        queryset = Carrier.objects.all()
        return queryset

    def retrieve(self, request, *args, **kwargs):

        # Grabbing the carrier code from the request and filtering by it
        carrier_code = self.request.parser_context['kwargs']['pk']
        try:
            instance = Carrier.objects.get(code=carrier_code)

        except Carrier.DoesNotExist:
            raise Http404

        serializer = CarrierSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        content = {'error': 'Forbidden method'}
        return Response(content, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['get', 'post'], detail=True, url_path='ratings', url_name='ratings')
    def ratings(self, request, *args, **kwargs):
        """
            Route for ratings
        """

        # Grabbing the carrier code from the request and filtering by it
        carrier_code = request.parser_context['kwargs']['pk']
        carrier = Carrier.objects.filter(code=carrier_code).first()

        if request.method == 'GET':
            item = CarrierRating.objects.filter(carrier=carrier).first()

            if not item:
                content = {'error': 'No rating fot this carrier yet...'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            serializer = CarrierRatingSerializer(item)
            return Response(serializer.data)

        elif request.method == 'POST':
            item = CarrierRating.objects.filter(carrier=carrier).first()

            if not item:
                item = CarrierRating.objects.create(
                    carrier=carrier,
                )

            # Grabbing the number of stars from the query
            stars = request.data.get('stars', None)

            if not stars:
                content = {'error': 'Number of stars not specified'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            if int(stars) < 1 or int(stars) > 5:
                content = {'error': 'Invalid numbers of stars'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            item.votes += 1
            item.total += int(stars)
            item.save()

            serializer = CarrierRatingSerializer(item)
            return Response(serializer.data)


class CarrierReviewSet(ModelViewSet):
    """
        View for adding/ retrieving reviews
    """
    model = CarrierReview
    serializer_class = CarrierReviewSerializer

    def get_renderers(self):
        return csv_renderer(self)

    def get_queryset(self):
        carrier_code = self.request.parser_context['kwargs']['parent_lookup_carriers']
        return CarrierReview.objects.filter(carrier__code=carrier_code)

    def create(self, request, *args, **kwargs):

        # Grabbing the carrier code and filtering later by it
        carrier_code = self.request.parser_context['kwargs']['parent_lookup_carriers']
        data = self.request.data

        # Grabbing the number of stars from the query of the request
        text = data.get('text', None)

        if not text:
            content = {'error': 'Field text is empty'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        carrier = Carrier.objects.filter(code=carrier_code).first()

        if carrier:
            item = CarrierReview.objects.create(
                carrier=carrier,
                text=text
            )
            serializer = CarrierReviewSerializer(item)
            return Response(serializer.data)


class AirportCarrierViewSet(ModelViewSet):
    """
        View for retrieving all the carriers operating at a given aiport
    """
    model = Carrier
    serializer_class = CarrierSerializer
    http_method_names = ['get']

    def get_renderers(self):
        return csv_renderer(self)

    def get_queryset(self, *args, **kwargs):
        # Grabbing the airport code from the request and filtering by it
        airport_code = self.request.parser_context['kwargs']['parent_lookup_airports']

        return Carrier.objects.filter(carrier_entries__airport__code=airport_code)

    def retrieve(self, request, *args, **kwargs):
        carrier_code = self.request.parser_context['kwargs']['pk']
        try:
            instance = Carrier.objects.get(code=carrier_code)

        except Carrier.DoesNotExist:
            raise Http404

        serializer = CarrierSerializer(instance)
        return Response(serializer.data)


class StatisticViewSet(ModelViewSet):
    """
        View for getting/ updating/ deleting statistics of a given month
    """
    model = Statistics
    serializer_class = StatisticsSerializer
    http_method_names = ['get', 'delete', 'patch']

    def get_renderers(self):
        return csv_renderer(self)

    def get_queryset(self, *args, **kwargs):

        # Grabbing the airport and carrier code
        airport_code = self.request.parser_context['kwargs']['parent_lookup_airports']
        carrier_code = self.request.parser_context['kwargs']['parent_lookup_operating_carriers']

        # Trying to grab the month and year from the query
        month = self.request.GET.get('month', None)
        year = self.request.GET.get('year', None)

        queryset = Statistics.objects.filter(statistics_entry__airport__code=airport_code,
                                             statistics_entry__carrier__code=carrier_code)

        # In case month and year were provided in the query, filter by them
        if month and year:
            queryset = queryset.filter(statistics_entry__time__month=month,
                                       statistics_entry__time__year=year)

        return queryset

    @action(methods=['delete', 'get'], detail=False, url_path='delete', url_name='delete')
    def delete(self, request, *args, **kwargs):
        airport_code = self.request.parser_context['kwargs']['parent_lookup_airports']
        carrier_code = self.request.parser_context['kwargs']['parent_lookup_operating_carriers']
        month = self.request.GET.get('month', None)
        year = self.request.GET.get('year', None)
        if not (month and year):
            content = {'error': 'Invalid syntax. Provide both year and month'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        item = Entry.objects.filter(carrier__code=carrier_code, airport__code=airport_code,
                                    time__month=month, time__year=year).first()

        if item:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        content = {'error': 'Resource not found'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get', 'patch'], detail=False, url_path='flights', url_name='flights')
    def flights(self, request, *args, **kwargs):

        airport_code = self.request.parser_context['kwargs']['parent_lookup_airports']
        carrier_code = self.request.parser_context['kwargs']['parent_lookup_operating_carriers']
        month = self.request.GET.get('month', None)
        year = self.request.GET.get('year', None)

        # Trying to grab "specific" term from the query
        # According to its value, use different serializer
        specific = self.request.GET.get('specific', None)

        if not (month and year):
            content = {'error': 'Invalid syntax. Provide both year and month'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        item = Flights.objects.filter(flights_statistics__statistics_entry__airport__code=airport_code,
                                      flights_statistics__statistics_entry__carrier__code=carrier_code,
                                      flights_statistics__statistics_entry__time__month=month,
                                      flights_statistics__statistics_entry__time__year=year).first()

        if not item:
            content = {'error': 'Resource not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':

            if specific == 'true':
                serializer = SpecificFlightsNumbersSerializer(item)
            else:
                serializer = FlightsSerializer(item)

            return Response(serializer.data)

        elif request.method == 'PATCH':
            # Trying to grab all the fields from the request and update
            # only the existent ones
            data = request.data

            cancelled = data.get('cancelled', None)
            on_time = data.get('on_time', None)
            total = data.get('total', None)
            delayed = data.get('delayed', None)
            diverted = data.get('diverted', None)

            if cancelled:
                item.cancelled = int(cancelled)
            if on_time:
                item.on_time = int(on_time)
            if total:
                item.total = int(total)
            if delayed:
                item.delayed = int(delayed)
            if diverted:
                item.diverted = int(diverted)
            item.save()

            serializer = FlightsSerializer(item)
            return Response(serializer.data)
    
    @action(methods=['get', 'patch'], detail=False, url_path='number-of-delays', url_name='number-of-delays')
    def number_of_delays(self, request, *args, **kwargs):

        airport_code = self.request.parser_context['kwargs']['parent_lookup_airports']
        carrier_code = self.request.parser_context['kwargs']['parent_lookup_operating_carriers']
        month = self.request.GET.get('month', None)
        year = self.request.GET.get('year', None)

        if not (month and year):
            content = {'error': 'Invalid syntax. Provide both year and month'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        item = NumberOfDelays.objects.filter(number_of_delays_statistics__statistics_entry__airport__code=airport_code,
                                             number_of_delays_statistics__statistics_entry__carrier__code=carrier_code,
                                             number_of_delays_statistics__statistics_entry__time__month=month,
                                             number_of_delays_statistics__statistics_entry__time__year=year).first()
        if not item:
            content = {'error': 'Resource not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':

            serializer = NumberOfDelaysSerializer(item)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            # Trying to grab all the fields from the request and update
            # only the existent ones
            data = request.data

            late_aircraft = data.get('late_aircraft', None)
            weather = data.get('weather', None)
            carrier = data.get('carrier', None)
            security = data.get('security', None)
            total = data.get('total', None)
            national_aviation_system = data.get('national_aviation_system', None)

            if late_aircraft:
                item.late_aircraft = int(late_aircraft)
            if weather:
                item.weather = int(weather)
            if carrier:
                item.carrier = int(carrier)
            if security:
                item.security = int(security)
            if total:
                item.total = int(total)
            if national_aviation_system:
                item.national_aviation_system = int(national_aviation_system)

            item.save()

            serializer = NumberOfDelaysSerializer(item)
            return Response(serializer.data)

    @action(methods=['get', 'patch'], detail=False, url_path='minutes-delayed', url_name='minutes-delayed')
    def minutes_delayed(self, request, *args, **kwargs):

        airport_code = self.request.parser_context['kwargs']['parent_lookup_airports']
        carrier_code = self.request.parser_context['kwargs']['parent_lookup_operating_carriers']
        month = self.request.GET.get('month', None)
        year = self.request.GET.get('year', None)

        if not (month and year):
            content = {'error': 'Invalid syntax. Provide both year and month'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        item = MinutesDelayed.objects.filter(minutes_delayed_statistics__statistics_entry__airport__code=airport_code,
                                             minutes_delayed_statistics__statistics_entry__carrier__code=carrier_code,
                                             minutes_delayed_statistics__statistics_entry__time__month=month,
                                             minutes_delayed_statistics__statistics_entry__time__year=year).first()
        if not item:
            content = {'error': 'Resource not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':

            serializer = MinutesDelayedSerializer(item)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            # Trying to grab all the fields from the request and update
            # only the existent ones
            data = request.data

            late_aircraft = data.get('late_aircraft', None)
            weather = data.get('weather', None)
            security = data.get('security', None)
            national_aviation_system = data.get('national_aviation_system', None)
            carrier = data.get('carrier', None)

            if late_aircraft:
                item.late_aircraft = int(late_aircraft)
            if weather:
                item.weather = int(weather)
            if security:
                item.security = int(security)
            if national_aviation_system:
                item.national_aviation_system = int(national_aviation_system)
            if carrier:
                item.carrier = int(carrier)
            item.save()

            serializer = NumberOfDelaysSerializer(item)
            return Response(serializer.data)


class DelaysMinutesViewSet(ModelViewSet):
    model = MinutesDelayed
    http_method_names = ['get']

    def get_renderers(self):
        return csv_renderer(self)

    def get_serializer_class(self):
        carrier_specific = self.request.GET.get('carrier-specific', None)

        if carrier_specific == "true":
            return MinutesDelayedCarrierSpecificSerializer
        else:
            return MinutesDelayedSerializer

    def get_queryset(self, *args, **kwargs):
        carrier_code = self.request.parser_context['kwargs']['parent_lookup_carriers']

        queryset = MinutesDelayed.objects.filter(
            minutes_delayed_statistics__statistics_entry__carrier__code=carrier_code)

        # Trying to grab month, year and airport code to filter by them
        month = self.request.GET.get('month', None)
        year = self.request.GET.get('year', None)
        airport = self.request.GET.get('airport', None)

        if airport:
            queryset = queryset.filter(minutes_delayed_statistics__statistics_entry__airport__code=airport)

        if month and year:
            queryset = queryset.filter(minutes_delayed_statistics__statistics_entry__time__month=int(month),
                                       minutes_delayed_statistics__statistics_entry__time__year=int(year))

        return queryset


class DescriptiveStatisticsViewSet(ModelViewSet):
    """
        Intermediary view for "CarriersDescriptiveStatistics"
    """
    serializer_class = StatisticsSerializer
    http_method_names = []


class DescriptiveStatisticsEndViewSet(ModelViewSet):
    """
           Intermediary view for "CarriersDescriptiveStatistics"
    """
    serializer_class = StatisticsSerializer
    http_method_names = []


class CarriersDescriptiveStatistics(ModelViewSet):
    serializer_class = DescriptiveStatisticsSerializer

    def get_renderers(self):
        return csv_renderer(self)

    def get_queryset(self):

        # Freeing the descriptive statistics table
        DescriptiveStatistics.objects.all().delete()

        # Grabbing the airports codes from the url
        a1 = self.request.parser_context['kwargs']['parent_lookup_descriptive_statistics']
        a2 = self.request.parser_context['kwargs']['parent_lookup_second_airport']

        query = Carrier.objects.filter(Q(carrier_entries__airport__code=a1) |
                                       Q(carrier_entries__airport__code=a2)).distinct()

        for x in query:
            query2 = MinutesDelayed.objects.filter(
                Q(minutes_delayed_statistics__statistics_entry__carrier=x) &
                (
                        Q(minutes_delayed_statistics__statistics_entry__airport__code=a1) |
                        Q(minutes_delayed_statistics__statistics_entry__airport__code=a2)
                )
            ).values_list('carrier', 'late_aircraft')

            # Building an array out of carrier and late_aircraft columns, summed up
            array = []

            for y in query2:
                array.append(y[0] + y[1])

            # In case there is more than 1 entry, generating a descriptive statistics object
            # Standard deviation can't be computed for only 1 entry
            if len(array) > 1:
                DescriptiveStatistics.objects.create(
                    mean=statistics.mean(array),
                    median=statistics.median(array),
                    standard_deviation=statistics.stdev(array),
                    carrier=x
                )

        return DescriptiveStatistics.objects.all()

    def retrieve(self, request, *args, **kwargs):

        carrier = kwargs['pk']

        item = self.get_queryset().filter(carrier__code=carrier).first()
        if item:
            serializer = DescriptiveStatisticsSerializer(item)
            return Response(serializer.data)
