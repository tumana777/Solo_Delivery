from django.contrib import admin
from django.utils.timezone import now

from .models import Branch, USAAddress, ChinaAddress, Country, Currency, Status, Flight
from django.utils.translation import gettext_lazy as _

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(USAAddress)
class USAAddressAdmin(admin.ModelAdmin):
    pass

@admin.register(ChinaAddress)
class ChinaAddressAdmin(admin.ModelAdmin):
    pass

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'transporting_price']

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields.remove('status')
            fields.remove('arrival_date')
        return fields

    list_display = [
        'country', 'formatted_departure_date',
        'formatted_estimated_arrival_date',
        'formatted_arrival_date', 'flight_number', 'status'
    ]

    actions = ['set_status_to_in_transit', 'set_status_to_arrived']

    def set_status_to_in_transit(self, request, queryset):
        status_in_transit = Status.objects.get(name="გზაშია")
        queryset.update(status=status_in_transit, arrival_date=None)
        self.message_user(request, _("რეის(ებ)ის სტატუსი განახლდა."))

    def set_status_to_arrived(self, request, queryset):
        status_arrived = Status.objects.get(name="ჩამოსულია")
        queryset.update(status=status_arrived, arrival_date=now().date())
        self.message_user(request, _("რეის(ებ)ის სტატუსი განახლდა."))

    set_status_to_in_transit.short_description = "სტატუსის შეცვლა - 'გზაშია'"
    set_status_to_arrived.short_description = "სტატუსის შეცვლა - 'ჩამოსულია'"

    def formatted_departure_date(self, obj):
        if obj.departure_date:
            return obj.departure_date.strftime('%d-%m-%Y')

    def formatted_estimated_arrival_date(self, obj):
        if obj.estimated_arrival_date:
            return obj.estimated_arrival_date.strftime('%d-%m-%Y')

    def formatted_arrival_date(self, obj):
        if obj.arrival_date:
            return obj.arrival_date.strftime('%d-%m-%Y')

    formatted_departure_date.short_description = _('გამოფრენა')
    formatted_estimated_arrival_date.short_description = _("ჩამოფრენის სავ.თარიღი")
    formatted_arrival_date.short_description = _("ჩამოფრენა")

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass