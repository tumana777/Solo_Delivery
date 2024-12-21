from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Parcel

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'tracking_number', 'country', 'status',
        'formatted_delivery_time', 'weight', 'custom_clearance',
        'transporting_fee', 'is_paid'
    )

    def formatted_delivery_time(self, obj):
        if obj.delivery_time:
            return obj.delivery_time.strftime('%d-%m-%Y')

    formatted_delivery_time.short_description = _('მისვლის თარიღი')