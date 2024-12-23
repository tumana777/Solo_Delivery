from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import FlightListSerializer, ParcelListSerializer, StatusListSerializer, ParcelCreateSerializer
from core.models import Flight, Status
from parcel.models import Parcel

class StatusListView(ListAPIView):
    serializer_class = StatusListSerializer
    queryset = Status.objects.all()

class FlightListView(ListAPIView):
    serializer_class = FlightListSerializer
    queryset = Flight.objects.all().select_related('status', 'country').order_by('-id')

class UserParcelListView(ListAPIView):
    serializer_class = ParcelListSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status__name']
    search_fields = ['tracking_number']

    def get_queryset(self):
        return Parcel.objects.filter(user=self.request.user).select_related(
            'status', 'flight', 'flight__status', 'flight__country',
            'country', 'category', 'currency', 'branch'
        )

class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_class = ParcelCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Parcel.objects.filter(
            user=self.request.user, status=Status.objects.get(name="მოლოდინშია")
        ).select_related( 'country', 'category', 'currency').order_by('-id')

    def perform_destroy(self, instance):
        if instance.status.name != "მოლოდინშია":
            return Response(
                {"detail": "You can only delete parcels with status 'მოლოდინშია'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance.delete()