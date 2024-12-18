from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, FormView

from core.models import ChinaAddress, USAAddress, Status
from parcel.models import Parcel
from user.forms import CustomUserCreationForm, UserBalanceUpdateForm
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

        total_transporting_fee = Parcel.objects.filter(
            user=self.request.user,
            status__name="ჩამოსულია",
            is_paid=False
        ).aggregate(total_fee=Sum('transporting_fee'))['total_fee']

        context['total_transporting_fee'] = total_transporting_fee or 0

        return context

class UpdateParcelStatusView(LoginRequiredMixin, UpdateView):
    model = Parcel
    fields = []
    login_url = reverse_lazy('user:login')

    def form_valid(self, form):
        status = get_object_or_404(Status, name="გატანილია")

        self.object.status = status
        self.object.taken_time = datetime.now()
        self.object.save()

        return redirect('user:room')

    def get_object(self, queryset=None):
        return get_object_or_404(Parcel, id=self.kwargs['pk'], user=self.request.user)

class UpdateParcelPaidView(LoginRequiredMixin, UpdateView):
    model = Parcel
    fields = []
    login_url = reverse_lazy('user:login')

    def form_valid(self, form):
        if self.object.user.balance < self.object.transporting_fee:
            return redirect('user:room')

        self.object.is_paid = True
        self.object.user.balance -= self.object.transporting_fee
        self.object.user.save()
        self.object.save()

        return redirect('user:room')

    def get_object(self, queryset=None):
        return get_object_or_404(Parcel, id=self.kwargs['pk'], user=self.request.user)

class UserBalanceUpdateView(LoginRequiredMixin, FormView):
    template_name = 'room.html'
    form_class = UserBalanceUpdateForm
    login_url = reverse_lazy('user:login')
    success_url = reverse_lazy('user:room')

    def form_valid(self, form):
        user = self.request.user
        amount = form.cleaned_data['amount']
        user.balance += amount
        user.save()
        messages.success(self.request, f"თქვენი ბალანსი განახლდა: +{amount:.2f}")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "გთხოვთ, შეიყვანეთ სწორი თანხა.")
        return super().form_invalid(form)