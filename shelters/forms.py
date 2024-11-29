from shelters.models import Animal, AdoptionApplication, Shelter
from django.core.exceptions import ValidationError
from users.models import CustomUser
from datetime import date
from django import forms



#FORM DE ANIMALES
class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'age', 'species', 'description', 'image', 'adoption_status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
 
#FORM DE LA SOLICITUD DE ADOPCIÓN       
class AdoptionApplicationCreationForm(forms.ModelForm):
    user = forms.CharField(max_length=255, label='Nombre completo')
    application_date = forms.DateField(initial=date.today)
    class Meta:
        model = AdoptionApplication
        fields = ('user', 'animal') #AÑADIR SHELTER!!!!!
        
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

class RegisterShelterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ['name', 'address', 'email', 'telephone', 'accreditation_file']

class UpdateShelterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ['name', 'address', 'telephone', 'email', 'accreditation_file', 'accreditation_status',
                   'register_date', 'status', 'latitude', 'longitude', 'postal_code']