import json
from django.core.management.base import BaseCommand
from api.models import (
    Time,
    NumberOfDelays,
    Flights,
    MinutesDelayed,
    Airport,
    Statistics,
    Entry,
    Carrier
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = json.load(open('airlines.json'))

        print(len(data))
        print(data[0])

        for x in range(int(len(data)/1000)):

            time = data[x]['time']

            year = time['year']
            month = time['month']
            label = time['label']

            time = Time.objects.create(
                month=month,
                year=year,
                label=label
            )

            statistics = data[x]['statistics']
            nr_delays = statistics['# of delays']

            nr_delays_carrier = nr_delays['carrier']
            nr_delays_late_aircraft = nr_delays['late aircraft']
            nr_delays_national_aviation_system = nr_delays['national aviation system']
            nr_delays_security = nr_delays['security']
            nr_delays_weather = nr_delays['weather']

            nr_delays = NumberOfDelays.objects.create(
                carrier=nr_delays_carrier,
                late_aircraft=nr_delays_late_aircraft,
                national_aviation_system=nr_delays_national_aviation_system,
                security=nr_delays_security,
                weather=nr_delays_weather
            )

            flights = statistics['flights']

            flights_cancelled = flights['cancelled']
            flights_delayed = flights['delayed']
            flights_diverted = flights['diverted']
            flights_on_time = flights['on time']
            flights_total = flights['total']

            flights = Flights.objects.create(
                cancelled=flights_cancelled,
                delayed=flights_delayed,
                diverted=flights_diverted,
                on_time=flights_on_time,
                total=flights_total
            )

            minutes_delayed = statistics['minutes delayed']

            minutes_delayed_carrier = minutes_delayed['carrier']
            minutes_delayed_late_aircraft = minutes_delayed['late aircraft']
            minutes_delayed_national_aviation_system = minutes_delayed['national aviation system']
            minutes_delayed_security = minutes_delayed['security']
            minutes_delayed_total = minutes_delayed['total']
            minutes_delayed_weather = minutes_delayed['weather']

            minutes_delayed = MinutesDelayed.objects.create(
                carrier=minutes_delayed_carrier,
                late_aircraft=minutes_delayed_late_aircraft,
                national_aviation_system=minutes_delayed_national_aviation_system,
                security=minutes_delayed_security,
                total=minutes_delayed_total,
                weather=minutes_delayed_weather
            )

            statistics = Statistics.objects.create(
                number_of_delays=nr_delays,
                flights=flights,
                minutes_delayed=minutes_delayed
            )

            airport = data[x]['airport']

            airport_code = airport['code']
            airport_name = airport['name']

            airport = Airport.objects.filter(code=airport_code).first()
            if not airport:
                airport = Airport.objects.create(
                    code=airport_code,
                    name=airport_name
                )

            carrier = data[x]['carrier']

            carrier_code = carrier['code']
            carrier_name = carrier['name']

            carrier = Carrier.objects.filter(code=carrier_code).first()
            if not carrier:
                carrier = Carrier.objects.create(
                    code=carrier_code,
                    name=carrier_name
                )

            entry = Entry.objects.create(
                statistics=statistics,
                time=time,
                airport=airport,
                carrier=carrier
            )





