from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Flight
from parcel.models import Parcel

@receiver(post_save, sender=Flight)
def update_parcels_on_flight_status_change(sender, instance, **kwargs):
    parcels = Parcel.objects.filter(flight=instance)

    for parcel in parcels:
        if parcel.status and parcel.status.name != "გატანილია":
            parcel.status = instance.status
            parcel.save()