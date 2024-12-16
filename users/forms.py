from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser, ShelterWorkerProfile
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
    full_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    birth_date = forms.DateField(required=True)
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'phone_number', 'birth_date', 'profile_picture', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtramos las opciones para ocultar 'admin'
        self.fields['user_type'].choices = [
            (value, label) for value, label in CustomUser.USER_TYPES if value != 'admin'
        ]

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'phone_number', 'birth_date', 'profile_picture', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtramos las opciones para ocultar 'admin'
        self.fields['user_type'].choices = [
            (value, label) for value, label in CustomUser.USER_TYPES if value != 'admin'
        ]
        

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Guardamos el request
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')


        if email and password:
            # Usamos authenticate, asegurándonos de pasar el 'email'
            user = authenticate(request=self.request, username=email, password=password)  # 'username' es 'email' aquí
            if user is None:
                raise forms.ValidationError("Email o contraseña incorrectos.")
            self.user = user
        return self.cleaned_data

# Formulario para las respuestas del test de compatibilidad de perros
class TestPerroForm(forms.Form):
    # Tamaño del perro
    tamaño = forms.ChoiceField(choices=[
        ('Pequeño', 'Pequeño (menos de 10 kg)'),
        ('Mediano', 'Mediano (10-25 kg)'),
        ('Grande', 'Grande (más de 25 kg)'),
        ('Sin preferencia', 'Sin preferencia'),
    ])

    # Edad del perro
    edad = forms.ChoiceField(choices=[
        ('Cachorro', 'Cachorro (menos de 1 año)'),
        ('Joven', 'Joven (1-3 años)'),
        ('Adulto', 'Adulto (3-7 años)'),
        ('Senior', 'Senior (más de 7 años)'),
        ('Sin preferencia', 'Sin preferencia'),
    ])

    # Nivel de energía
    energia = forms.ChoiceField(choices=[
        ('Baja', 'Baja'),
        ('Moderada', 'Moderada'),
        ('Alta', 'Alta'),
    ])

    # Tipo de pelaje
    pelaje = forms.ChoiceField(choices=[
        ('Pelo corto', 'Pelo corto y fácil de mantener'),
        ('Pelo largo', 'Pelo largo y que requiere mantenimiento'),
        ('Hipoalergénico', 'Hipoalergénico'),
        ('Sin preferencia', 'Sin preferencia'),
    ])

    # Temperamento
    temperamento = forms.ChoiceField(choices=[
        ('Tranquilo', 'Tranquilo y relajado'),
        ('Activo', 'Activo y juguetón'),
        ('Protector', 'Protector y vigilante'),
        ('Sin preferencia', 'Sin preferencia'),
    ])

    # Necesidad de ejercicio
    ejercicio = forms.ChoiceField(choices=[
        ('Poco', 'Poco (paseos cortos)'),
        ('Moderado', 'Moderado (paseos largos)'),
        ('Alto', 'Alto (mucho ejercicio físico)'),
        ('Sin preferencia', 'Sin preferencia'),
    ])

    # Espacio disponible en casa
    espacio = forms.ChoiceField(choices=[
        ('Pequeño', 'Vivo en un apartamento o espacio pequeño'),
        ('Mediano', 'Tengo un jardín pequeño o patio'),
        ('Grande', 'Tengo un jardín grande o terreno amplio'),
        ('Sin preferencia', 'Sin preferencia'),
    ])

    # Compatibilidad con niños
    niños = forms.ChoiceField(choices=[
        ('Sí', 'Sí, es importante que se lleve bien con niños'),
        ('No', 'No me importa si no se lleva bien con niños'),
        ('Indiferente', 'Indiferente'),
    ])

    # Compatibilidad con otros perros
    otros_perros = forms.ChoiceField(choices=[
        ('Sí', 'Sí, debe llevarse bien con otros perros'),
        ('No', 'No, prefiero que sea un perro solitario'),
        ('Indiferente', 'Indiferente'),
    ])

    # Necesidad de compañía
    compañía = forms.ChoiceField(choices=[
        ('Alta', 'Alta (necesita estar acompañado todo el tiempo)'),
        ('Moderada', 'Moderada (puede quedarse solo por un rato)'),
        ('Baja', 'Baja (puede estar solo por períodos largos)'),
    ])

# Formulario para las respuestas del test de compatibilidad de gatos
class TestGatoForm(forms.Form):
    # Tamaño del gato
    tamaño = forms.ChoiceField(choices=[
        ('Pequeño', 'Pequeño (menos de 5 kg)'),
        ('Mediano', 'Mediano (5-8 kg)'),
        ('Grande', 'Grande (más de 8 kg)'),
        ('Sin preferencia', 'Sin preferencia'),
    ])

    # Edad del gato
    edad = forms.ChoiceField(choices=[
        ('Cachorro', 'Cachorro (menos de 1 año)'),
        ('Joven', 'Joven (1-3 años)'),
        ('Adulto', 'Adulto (3-7 años)'),
        ('Senior', 'Senior (más de 7 años)'),
        ('Sin preferencia', 'Sin preferencia'),
    ])

    # Nivel de actividad
    actividad = forms.ChoiceField(choices=[
        ('Baja', 'Baja (prefiere descansar todo el día)'),
        ('Moderada', 'Moderada (le gusta jugar pero también descansar)'),
        ('Alta', 'Alta (le encanta jugar y explorar todo el tiempo)'),
    ])

    # Tipo de pelaje
    pelaje = forms.ChoiceField(choices=[
        ('Corto', 'Corto (requiere poco mantenimiento)'),
        ('Largo', 'Largo (requiere mucho mantenimiento)'),
        ('Hipoalergénico', 'Hipoalergénico'),
        ('Sin preferencia', 'Sin preferencia'),
    ])

    # Personalidad
    personalidad = forms.ChoiceField(choices=[
        ('Independiente', 'Independiente (le gusta estar solo a veces)'),
        ('Cariñoso', 'Cariñoso (le gusta estar con su dueño todo el tiempo)'),
        ('Juguetón', 'Juguetón (le gusta mucho jugar y interactuar)'),
        ('Sin preferencia', 'Sin preferencia'),
    ])

    # Necesidad de espacio
    espacio = forms.ChoiceField(choices=[
        ('Pequeño', 'Vivo en un apartamento o espacio pequeño'),
        ('Mediano', 'Tengo algo de espacio pero no mucho'),
        ('Grande', 'Tengo un jardín grande o terreno amplio'),
        ('Sin preferencia', 'Sin preferencia'),
    ])

    # Compatibilidad con niños
    niños = forms.ChoiceField(choices=[
        ('Sí', 'Sí, debe llevarse bien con niños'),
        ('No', 'No me importa si no se lleva bien con niños'),
        ('Indiferente', 'Indiferente'),
    ])

    # Compatibilidad con otros gatos
    otros_gatos = forms.ChoiceField(choices=[
        ('Sí', 'Sí, debe llevarse bien con otros gatos'),
        ('No', 'No, prefiero que sea un gato solitario'),
        ('Indiferente', 'Indiferente'),
    ])

    # Necesidad de compañía
    compañía = forms.ChoiceField(choices=[
        ('Alta', 'Alta (necesita compañía casi todo el tiempo)'),
        ('Moderada', 'Moderada (puede estar solo por un rato)'),
        ('Baja', 'Baja (puede estar solo por períodos largos)'),
    ])

class WorkerRegistrationForm(forms.ModelForm):
    # Campos para el CustomUser
    user = forms.CharField(max_length=255, label="Nombre de usuario")
    email = forms.EmailField(label="Correo electrónico")
    full_name = forms.CharField(max_length=255, label="Nombre completo")

    class Meta:
        model = ShelterWorkerProfile
        fields = ['user', 'email', 'full_name', 'shelter', 'position']
    
    def clean_user(self):
        # Validar si el nombre de usuario ya existe en el sistema
        username = self.cleaned_data.get('user')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def save(self, commit=True):
        # Crear un nuevo CustomUser
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['user'],
            email=self.cleaned_data['email'],
            full_name=self.cleaned_data['full_name'],
            password="contraseña_temporal",  # Asegúrate de enviar un correo para cambiar la contraseña.
        )
        
        # Crear el perfil de trabajador
        worker_profile = super().save(commit=False)
        worker_profile.user = user
        if commit:
            worker_profile.save()
        return worker_profile 