from django.urls import path
from .views import UserRegistrationView, UserAddressesView
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'user'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html', next_page='core:index'), name='login'),
    path('addresses/', UserAddressesView.as_view(), name='user_addresses'),
    path('logout/', LogoutView.as_view(next_page='user:login'), name='logout'),
]