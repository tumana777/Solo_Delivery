from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from api.serializers import FlightListSerializer, ParcelListSerializer, StatusListSerializer, ParcelCreateSerializer
from core.models import Flight, Status
from parcel.models import Parcel


@extend_schema_view(
    get=extend_schema(
        summary="List all statuses",
        description="Retrieve a list of all statuses available in the system.",
        responses={200: StatusListSerializer(many=True)}
    )
)
class StatusListView(ListAPIView):
    serializer_class = StatusListSerializer
    queryset = Status.objects.all()


@extend_schema_view(
    get=extend_schema(
        summary="List all flights",
        description="Retrieve a list of all flights with their associated statuses and countries.",
        responses={200: FlightListSerializer(many=True)}
    )
)
class FlightListView(ListAPIView):
    serializer_class = FlightListSerializer
    queryset = Flight.objects.all().select_related('status', 'country').order_by('-id')


@extend_schema_view(
    get=extend_schema(
        summary="List user-specific parcels",
        description="Retrieve a list of parcels belonging to the authenticated user, filtered by status or searched by tracking number.",
        responses={200: ParcelListSerializer(many=True)}
    )
)
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


@extend_schema_view(
    list=extend_schema(
        summary="List user's waiting parcels",
        description="Retrieve a list of parcels with status 'მოლოდინშია' for the authenticated user.",
        responses={200: ParcelCreateSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Create a new parcel",
        description="Create a new parcel associated with the authenticated user and assign it the status 'მოლოდინშია'.",
        responses={201: ParcelCreateSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a parcel",
        description="Delete a parcel only if its status is 'მოლოდინშია'.",
        responses={
            204: None,
            400: "You can only delete parcels with status 'მოლოდინშია'."
        }
    ),
)
class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_class = ParcelCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Parcel.objects.filter(
            user=self.request.user, status=Status.objects.get(name="მოლოდინშია")
        ).select_related('country', 'category', 'currency').order_by('-id')

    def perform_destroy(self, instance):
        if instance.status.name != "მოლოდინშია":
            return Response(
                {"detail": "You can only delete parcels with status 'მოლოდინშია'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance.delete()
