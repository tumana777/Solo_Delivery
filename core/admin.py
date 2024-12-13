from django.contrib import admin
from .models import Branch, USAAddress, ChinaAddress

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(USAAddress)
class USAAddressAdmin(admin.ModelAdmin):
    pass

@admin.register(ChinaAddress)
class ChinaAddressAdmin(admin.ModelAdmin):
    pass
