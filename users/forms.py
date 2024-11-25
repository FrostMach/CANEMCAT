from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
    full_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    birth_date = forms.DateField(required=True)
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'phone_number', 'birth_date', 'profile_picture', 'user_type')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'phone_number', 'birth_date', 'profile_picture', 'user_type')
        
