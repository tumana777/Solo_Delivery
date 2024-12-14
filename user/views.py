from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from core.models import ChinaAddress, USAAddress
from user.forms import CustomUserCreationForm
from user.models import CustomUser

class UserRegistrationView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('user:login')

class UserAddressesView(TemplateView):
    template_name = 'addresses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        china_static_address = ChinaAddress.objects.all().select_related('country').first()
        usa_static_address = USAAddress.objects.all().select_related('country').first()

        china_address = {
            "price": china_static_address.country.transporting_price,
            "name": f"{self.request.user.first_name_en} {self.request.user.last_name_en}",
            "address": f"{china_static_address.address}{self.request.user.room_number}",
            "street": china_static_address.street,
            "district": china_static_address.district,
            "city": china_static_address.city,
            "province": china_static_address.province,
            "zip": china_static_address.zip_code,
            "phone": china_static_address.cell_phone,
        }

        usa_address = {
            "price": usa_static_address.country.transporting_price,
            "name": f"{self.request.user.first_name_en} {self.request.user.last_name_en}",
            "address1": usa_static_address.address_1,
            "address2": self.request.user.room_number,
            "city": usa_static_address.city,
            "state": usa_static_address.state,
            "zip": usa_static_address.zip_code,
            "phone": usa_static_address.cell_phone,
        }

        # Add data to the context
        context['china_address'] = china_address
        context['usa_address'] = usa_address

        return context
