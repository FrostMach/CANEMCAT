import re
from shelters.models import Animal, AdoptionApplication, Shelter
from django.core.exceptions import ValidationError
from users.models import CustomUser
from datetime import date
from django import forms

#FORM DE ANIMALES
class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = [
            'name', 'species', 'sex', 'age', 'size', 
            'personality', 'energy', 'fur', 'description', 
            'image', 'adoption_status', 'shelter'
        ]
        labels = {
            'name': 'Nombre',
            'species': 'Especie',
            'sex': 'Sexo',
            'age': 'Edad',
            'size': 'Tamaño',
            'personality': 'Personalidad',
            'energy': 'Nivel de energía',
            'fur': 'Pelaje',
            'description': 'Descripción',
            'image': 'Imagen',
            'adoption_status': 'Estado de adopción',
            'shelter': 'Protectora',
        }
 
class AnimalFilterForm(forms.Form):
    species = forms.ChoiceField(
        choices=[('', '---')] + Animal.SPECIES,  # Agrega opción vacía para no filtrar
        required=False,
        label="Especie"
    )
    sex = forms.ChoiceField(
        choices=[('', '---')] + Animal.SEX,
        required=False,
        label="Sexo"
    )
    size = forms.ChoiceField(
        choices=[('', '---')] + Animal.SIZE,
        required=False,
        label="Tamaño"
    )
    adoption_status = forms.ChoiceField(
        choices=[('', '---')] + Animal.ADOPTION_STATUS,
        required=False,
        label="Estado de adopción"
    )
    shelter = forms.ModelChoiceField(
        queryset=Shelter.objects.all(),
        required=False,
        label="Protectora",
        empty_label="---"
    )

    def __init__(self, *args, **kwargs):
        # Permitir que se pase un queryset personalizado para el campo 'shelter'
        shelter_queryset = kwargs.pop('shelter_queryset', Shelter.objects.all())
        super().__init__(*args, **kwargs)
        self.fields['shelter'].queryset = shelter_queryset
 
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

        def clean(self):
            cleaned_data = super().clean()
            name = cleaned_data.get('name')
            telephone = cleaned_data.get('telephone')
            email = cleaned_data.get('email')

            # Validación del teléfono: Asegurarse de que tenga al menos 9 dígitos
            if telephone:
                if not telephone.isdigit():
                    self.add_error('telephone', 'El teléfono solo debe contener números.')
                elif len(str(telephone)) < 9:
                    self.add_error('telephone', 'El teléfono debe tener una longitud mínima de 9 dígitos.')

            # Validación del nombre: No permitir que contenga la palabra "admin"
            if name and 'admin' in name.lower():
                self.add_error('name', 'El nombre no puede contener "admin".')

            # Validación de correo electrónico: Verificar si ya está registrado
            if email and Shelter.objects.filter(email=email).exists():
                self.add_error('email', 'Este correo electrónico ya está registrado.')

            return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Validación del formato del correo electrónico
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("El correo electrónico no tiene un formato válido.")
        return email

    def clean_accreditation_file(self):
        accreditation_file = self.cleaned_data.get('accreditation_file')

        # Validar que se haya subido un archivo si es necesario
        if not accreditation_file:
            raise ValidationError("Debe subir un archivo de acreditación.")
        return accreditation_file
        
class CompleteShelterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ['latitude', 'longitude', 'postal_code']

        def clean_latitude(self):
            latitude = self.cleaned_data.get('latitude')
            
            if latitude and not (-90 <= latitude <= 90):
                raise ValidationError('La latitud debe estar entre -90 y 90.')
            return latitude

        def clean_longitude(self):
            longitude = self.cleaned_data.get('longitude')

            if longitude and not (-180 <= longitude <= 180):
                raise ValidationError('La longitud debe estar entre -180 y 180.')
            return longitude
        
        def clean(self):
            cleaned_data = super().clean()
            
            # Revisamos si alguno de los campos requeridos está vacío
            required_fields = ['latitude', 'longitude', 'postal_code']
            
            for field in required_fields:
                value = cleaned_data.get(field)
                if not value:
                    raise ValidationError(f"El campo {field} es obligatorio.")
            
            return cleaned_data
        
class UpdateShelterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ['name', 'address', 'telephone', 'email', 'accreditation_file', 'status',
                   'latitude', 'longitude', 'postal_code']
        
    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        if latitude is not None:
            if latitude < -90 or latitude > 90:
                raise ValidationError("La latitud debe estar entre -90 y 90 grados.")
        return latitude
    
    # Validación personalizada para longitud
    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        if longitude is not None:
            if longitude < -180 or longitude > 180:
                raise ValidationError("La longitud debe estar entre -180 y 180 grados.")
        return longitude
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Revisamos si alguno de los campos requeridos está vacío
        required_fields = ['name', 'address', 'telephone', 'email', 'accreditation_file', 'status', 'latitude', 'longitude', 'postal_code']
        
        for field in required_fields:
            value = cleaned_data.get(field)
            if not value:
                raise ValidationError(f"El campo {field} es obligatorio.")
        
        return cleaned_data