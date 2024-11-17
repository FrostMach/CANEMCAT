from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,AdoptionApplication
from django.core.exceptions import ValidationError
from datetime import date

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'phone_number', 'address', 'birth_date', 'profile_picture')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'phone_number', 'address', 'birth_date', 'profile_picture')
        
class AdoptionApplicationCreationForm(forms.ModelForm):
    user = forms.CharField(max_length=255, label='Nombre completo')

    application_date = forms.DateField(initial=date.today)
    class Meta:
        model = AdoptionApplication
        fields = ('user', 'animal', 'center')
        
    def clean_user(self):
    # Obtener el valor del campo 'user' (nombre completo)
        user_name = self.cleaned_data['user']

        # Intentar obtener un usuario que coincida con el nombre completo ingresado
        try:
            user = CustomUser.objects.get(full_name=user_name)
        except CustomUser.DoesNotExist:
            raise ValidationError("El nombre ingresado no corresponde a un usuario registrado.")
        
        return user  # Devolvemos el usuario encontrado

    def save(self, commit=True):
        # Guardamos la solicitud de adopción con el usuario encontrado
        instance = super().save(commit=False)
        instance.user = self.cleaned_data['user']  # Asociamos el usuario al modelo
        if 'application_date' in self.cleaned_data:
            instance.application_date = self.cleaned_data['application_date']
        else:
            instance.application_date = date.today()  # Asignamos la fecha actual si no se especificó

        if commit:
            instance.save()
        return instance

# class EncuestaForm(forms.ModelForm):
#     class Meta:
#         model = RespuestaEncuesta
#         fields = ['cuidados_respuesta', 'experiencia_respuesta', 'tiempo_respuesta', 'vivienda_respuesta', 'otras_observaciones_respuesta']
#         widgets = {
#             'cuidados_respuesta': forms.Textarea(attrs={'rows': 3}),
#             'experiencia_respuesta': forms.Textarea(attrs={'rows': 3}),
#             'otras_observaciones_respuesta': forms.Textarea(attrs={'rows': 3}),
#         }