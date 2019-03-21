"""airlines_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework_extensions.routers import ExtendedDefaultRouter

from api.views import (
    AirportViewSet,
    CarrierViewSet,
    AirportCarrierViewSet,
    StatisticViewSet,
    DelaysMinutesViewSet,
    DescriptiveStatisticsViewSet,
    DescriptiveStatisticsEndViewSet,
    CarriersDescriptiveStatistics,
    CarrierReviewSet,
)

router = ExtendedDefaultRouter()

airports = router.register(r'airports', AirportViewSet, base_name='airports')

operating_carriers = airports.register(r'carriers', AirportCarrierViewSet,
                                       base_name='airport-carriers',
                                       parents_query_lookups=['airports'])

statistics = operating_carriers.register(r'statistics', StatisticViewSet,
                                         base_name='statistics',
                                         parents_query_lookups=['airports',
                                                                'operating_carriers'],)

carriers = router.register(r'carriers', CarrierViewSet, base_name='carriers')

delays_minutes = carriers.register(r'delays-minutes', DelaysMinutesViewSet,
                                   base_name="delays_minutes",
                                   parents_query_lookups=['carriers'],)

review = carriers.register(r'reviews', CarrierReviewSet, base_name='reviews',
                           parents_query_lookups=['carriers'])

descriptive_statistics = router.register(r'descriptive-statistics', DescriptiveStatisticsViewSet,
                                         base_name='descriptive_statistics')


second_airport = descriptive_statistics.register(r'second-airport', DescriptiveStatisticsEndViewSet,
                                                 base_name='second_airport',
                                                 parents_query_lookups=['descriptive_statistics'])


carriers_descriptive_statistics = second_airport.register(r'carriers', CarriersDescriptiveStatistics,
                                                          base_name='carriers_descriptive_statistics',
                                                          parents_query_lookups=['descriptive_statistics',
                                                                                 'second_airport'],)


urlpatterns = [
    url(r'^api/', include(router.urls), name='api'),
    url(r'^admin/', admin.site.urls),
]















