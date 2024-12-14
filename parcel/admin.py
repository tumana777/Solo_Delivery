from django.contrib import admin

from .models import Category, Parcel

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'tracking_number', 'country', 'status',
        'delivery_time', 'weight', 'custom_clearance',
        'transporting_fee', 'is_paid'
    )
