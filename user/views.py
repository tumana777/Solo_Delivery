from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, UpdateView

from core.models import ChinaAddress, USAAddress, Status
from parcel.models import Parcel
from user.forms import CustomUserCreationForm
from user.models import CustomUser

class UserRegistrationView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('user:login')

class UserAddressesView(LoginRequiredMixin, TemplateView):
    template_name = 'addresses.html'
    login_url = reverse_lazy('user:login')

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

class UserParcelsView(LoginRequiredMixin, ListView):
    model = Parcel
    template_name = 'room.html'
    context_object_name = 'parcels'
    login_url = 'user:login'

    def get_queryset(self):
        status_filter = self.request.GET.get('status', 'საწყობშია')
        queryset = Parcel.objects.filter(user=self.request.user).select_related('flight', 'status', 'country')

        if status_filter:
            queryset = queryset.filter(status__name=status_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', 'საწყობშია')

        return context

class UpdateParcelStatusView(LoginRequiredMixin, UpdateView):
    model = Parcel
    fields = []
    login_url = reverse_lazy('user:login')

    def form_valid(self, form):
        status = get_object_or_404(Status, name="გატანილია")

        self.object.status = status
        self.object.save()

        return redirect('user:room')

    def get_object(self, queryset=None):
        return get_object_or_404(Parcel, id=self.kwargs['pk'], user=self.request.user)

