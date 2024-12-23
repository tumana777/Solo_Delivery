from rest_framework import serializers
from core.models import Flight, Status
from parcel.models import Parcel

class StatusListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class FlightListSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='status.name')
    country = serializers.ReadOnlyField(source='country.name')

    class Meta:
        model = Flight
        fields = '__all__'

class ParcelListSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='status.name')
    flight = FlightListSerializer(read_only=True)
    country = serializers.ReadOnlyField(source='country.name')
    category = serializers.ReadOnlyField(source='category.name')
    currency = serializers.ReadOnlyField(source='currency.name')
    branch = serializers.ReadOnlyField(source='branch.name')

    class Meta:
        model = Parcel
        fields = [
            'id', 'tracking_number', 'status', 'country',
            'category', 'price', 'currency', 'online_store', 'branch',
            'delivery_time', 'weight', 'transporting_fee', 'is_paid',
            'is_declared', 'custom_clearance', 'created_at', 'updated_at',
            'flight', 'taken_time'
        ]

class ParcelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = [
            'id', 'tracking_number', 'country', 'weight',
            'category', 'price', 'currency', 'online_store'
        ]

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        validated_data['user'] = user
        validated_data['status'] = Status.objects.get(name="მოლოდინშია")

        return super().create(validated_data)