from django import forms

from parcel.models import Parcel


class ParcelDeclareForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ['tracking_number', 'category', 'price', 'currency', 'online_store', 'branch']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tracking_number'].disabled = True