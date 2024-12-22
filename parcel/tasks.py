from celery import shared_task
from parcel.models import Parcel

@shared_task
def process_paid_parcels():
    parcels = Parcel.objects.filter(status__name="ჩამოსულია", is_paid=False)

    for parcel in parcels:
        user = parcel.user
        if user.balance >= parcel.transporting_fee:
            user.balance -= parcel.transporting_fee
            user.save()

            parcel.is_paid = True
            parcel.save()

            print(f"Parcel {parcel.tracking_number} marked as paid and user balance updated.")
