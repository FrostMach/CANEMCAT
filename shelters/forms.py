
from django import forms

from .models import Shelter


class RegisterShelterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ['name', 'address', 'email', 'telephone', 'accreditation_file']

class UpdateShelterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ['name', 'address', 'telephone', 'email', 'accreditation_file', 'accreditation_status', 'register_date', 'status']