from django.urls import path, include
from rest_framework import routers

from .views import FlightListView, UserParcelListView, StatusListView, ParcelViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('waiting_parcels', ParcelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('statusses/', StatusListView.as_view(), name='status'),
    path('flights/', FlightListView.as_view(), name='flights'),
    path('parcels/', UserParcelListView.as_view(), name='parcels'),
]