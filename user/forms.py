from django import forms
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('პაროლი'),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_('გაიმეორეთ პაროლი'),
        widget=forms.PasswordInput,
    )

    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name_ka', 'last_name_ka', 'first_name_en',
            'last_name_en', 'personal_ID', 'address', 'branch', 'phone_number'
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        validate_password(password1)
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserBalanceUpdateForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label="თანხა",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
    )