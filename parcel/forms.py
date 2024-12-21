from django import forms
from parcel.models import Parcel
from django.utils.translation import gettext_lazy as _

class ParcelAddForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ['tracking_number', 'country', 'weight', 'category', 'price', 'currency', 'online_store']
        labels = {
            'weight': _('სავარაუდო წონა'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
            field.widget.attrs['required'] = 'required'

class ParcelDeclareForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ['category', 'price', 'currency', 'online_store', 'branch']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
            field.widget.attrs['required'] = 'required'