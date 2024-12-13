from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name_ka', 'last_name_ka', 'is_active', 'is_staff', 'is_superuser')
    readonly_fields = ['room_number']