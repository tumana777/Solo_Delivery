from django.urls import path
from .views import (
    UserRegistrationView, UserAddressesView, UserParcelsView,
    ParcelStatusUpdateView, ParcelPaidUpdateView, UserBalanceUpdateView,
    UserParcelDeclareView, AddParcelView, UserParcelDeleteView
)
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'user'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html', next_page='core:index'), name='login'),
    path('addresses/', UserAddressesView.as_view(), name='user_addresses'),
    path('logout/', LogoutView.as_view(next_page='user:login'), name='logout'),
    path('room/parcels/', UserParcelsView.as_view(), name='room'),
    path('parcel/<int:pk>/update_status/', ParcelStatusUpdateView.as_view(), name='update_parcel_status'),
    path('parcel/<int:pk>/update_paid/', ParcelPaidUpdateView.as_view(), name='update_parcel_paid'),
    path('update_balance/', UserBalanceUpdateView.as_view(), name='update_balance'),
    path('parcel/<int:pk>/update/', UserParcelDeclareView.as_view(), name='update_parcel'),
    path('add_parcel/', AddParcelView.as_view(), name='add_parcel'),
    path('parcel/<int:pk>/delete/', UserParcelDeleteView.as_view(), name='delete_parcel'),
]