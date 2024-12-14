from django.contrib import admin
from .models import Branch, USAAddress, ChinaAddress, Country, Currency, Status, Flight

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
    list_display = ['country', 'departure_date', 'estimated_arrival_date', 'arrival_date', 'flight_number', 'status']

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass