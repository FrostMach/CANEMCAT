from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Animal

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'phone_number', 'address', 'birth_date', 'profile_picture')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'phone_number', 'address', 'birth_date', 'profile_picture')

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'age', 'species', 'description', 'image', 'adoption_status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

#, 'shelter'