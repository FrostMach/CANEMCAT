from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomUser, ShelterWorkerProfile
from django.contrib.auth.forms import AuthenticationForm
from datetime import date
# Este formulario ya está incluido en Django, solo necesitas importarlo.
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
    full_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    birth_date = forms.DateField(required=True)
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'phone_number', 'birth_date', 'profile_picture', 'user_type')
        
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                raise ValidationError('Tienes que ser mayor de edad para poder darte de alta')
        return birth_date

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
class TestPerroShortForm(forms.Form):
    paseo = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Menos de 1 hora", "Menos de 1 hora"), ("Entre 1 y 3 horas", "Entre 1 y 3 horas"), ("Más de 3 horas", "Más de 3 horas")],
        label="1. ¿Cuánto tiempo al día estarás disponible para interactuar con el perro?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(1)"})
    )

    independiente = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Muy importante", "Muy importante"), ("Moderadamente importante", "Moderadamente importante"), ("No es importante", "No es importante")],
        label="2. ¿Qué tan importante es para ti que el perro sea independiente cuando no estás en casa?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(2)"})
    )

    familia = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Sí, niños pequeños (menos de 12 años)", "Sí, niños pequeños (menos de 12 años)"), ("Sí, personas mayores", "Sí, personas mayores"), ("No", "No")],
        label="3. ¿Hay niños o personas mayores en el hogar?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(3)"})
    )

    costos = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Muy dispuesto", "Muy dispuesto"), ("Moderadamente dispuesto", "Moderadamente dispuesto"), ("Prefiero evitarlo", "Prefiero evitarlo")],
        label="4. ¿Qué tan dispuesto estás a asumir los costos de cuidados específicos como alimento especializado o tratamientos médicos frecuentes?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(4)"})
    )

    tolerante = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Muy tolerante", "Muy tolerante"), ("Moderadamente tolerante", "Moderadamente tolerante"), ("Poco tolerante", "Poco tolerante")],
        label="5. ¿Qué tan tolerante eres con comportamientos como arañar muebles o ladrar frecuentemente?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(5)"})
    )

    vivienda = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Casa con jardín o terraza", "Casa con jardín o terraza"), ("Apartamento pequeño", "Apartamento pequeño"), ("Apartamento grande", "Apartamento grande")],
        label="6. ¿Dónde vives actualmente?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(6)"})
    )

    espacio_especifico = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Sí, totalmente dispuesto", "Sí, totalmente dispuesto"), ("Sí, pero con limitaciones", "Sí, pero con limitaciones"), ("No", "No")],
        label="7. ¿Estás dispuesto a crear espacios específicos para el perro, como camas o áreas de juego?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(7)"})
    )

    exterior_interior = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Exterior", "Exterior"), ("Interior", "Interior"), ("Ambos", "Ambos")],
        label="8. ¿Prefieres un perro que pueda salir al exterior o que sea exclusivamente de interior?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(8)"})
    )

    adaptacion = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Sí, completamente dispuesto", "Sí, completamente dispuesto"), ("Moderadamente dispuesto", "Moderadamente dispuesto"), ("No estoy seguro", "No estoy seguro")],
        label="9. ¿Estás dispuesto a lidiar con periodos de adaptación si el perro es tímido o reservado al principio?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(9)"})
    )

    porque_adoptar = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Compañía emocional", "Compañía emocional"), ("Ayudar a un animal que lo necesita", "Ayudar a un animal que lo necesita"), ("Tener una presencia tranquila en casa", "Tener una presencia tranquila en casa"), ("Otros", "Otros")],
        label="10. ¿Por qué quieres adoptar un perro?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(10)"})
    )

    situaciones_imprevistas = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Me adapto fácilmente", "Me adapto fácilmente"), ("Me cuesta pero intento resolverlo", "Me cuesta pero intento resolverlo"), ("Prefiero evitar complicaciones", "Prefiero evitar complicaciones")],
        label="11. ¿Cómo manejas situaciones estresantes o imprevistas con una mascota?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(11)"})
    )

    carinoso = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Muy importante", "Muy importante"), ("Moderadamente importante", "Moderadamente importante"), ("Poco importante", "Poco importante")],
        label="12. ¿Qué tan importante es para ti que el perro sea cariñoso contigo?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(12)"})
    )

    enriquecer = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Reduciendo el estrés", "Reduciendo el estrés"), ("Proporcionando compañía", "Proporcionando compañía"), ("Como un nuevo pasatiempo o responsabilidad", "Como un nuevo pasatiempo o responsabilidad")],
        label="13. ¿Cómo crees que un perro puede enriquecer tu vida?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(13)"})
    )

    conexion_emocional = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Un vínculo cercano y constante", "Un vínculo cercano y constante"), ("Una relación tranquila pero no muy intensa", "Una relación tranquila pero no muy intensa"), ("Independencia mutua", "Independencia mutua")],
        label="14. ¿Qué tipo de conexión emocional esperas tener con el perro?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(14)"})
    )

    que_valoras = forms.ChoiceField(
        choices=[("", "Selecciona una opción"), ("Su carácter y personalidad", "Su carácter y personalidad"), ("Su apariencia física", "Su apariencia física"), ("Su capacidad de adaptarse a mi estilo de vida", "Su capacidad de adaptarse a mi estilo de vida")],
        label="15. ¿Qué valoras más en una mascota?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(15)"})
    )


class TestGatoShortForm(forms.Form):
    # Pregunta 1: ¿Cuánto tiempo al día estarás disponible para interactuar con el gato?
    interactuar = forms.ChoiceField(
        choices=[
            ('Menos de 1 hora', 'Menos de 1 hora'),
            ('Entre 1 y 3 horas', 'Entre 1 y 3 horas'),
            ('Más de 3 horas', 'Más de 3 horas'),
        ],
        label="1. ¿Cuánto tiempo al día estarás disponible para interactuar con el gato?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(1)"})

    )

    # Pregunta 2: ¿Qué tan importante es para ti que el gato sea independiente cuando no estás en casa?
    independiente = forms.ChoiceField(
        choices=[
            ('Muy importante', 'Muy importante'),
            ('Moderadamente importante', 'Moderadamente importante'),
            ('No es importante', 'No es importante'),
        ],
        label="2. ¿Qué tan importante es para ti que el gato sea independiente cuando no estás en casa?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(2)"})

    )

    # Pregunta 3: ¿Hay niños o personas mayores en el hogar?
    familia = forms.ChoiceField(
        choices=[
            ('Sí, niños pequeños (menos de 12 años)', 'Sí, niños pequeños (menos de 12 años)'),
            ('Sí, personas mayores', 'Sí, personas mayores'),
            ('No', 'No'),
        ],
        label="3. ¿Hay niños o personas mayores en el hogar?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(3)"})

    )

    # Pregunta 4: ¿Qué tan dispuesto estás a asumir los costos de cuidados específicos como alimento especializado o tratamientos médicos frecuentes?
    costos = forms.ChoiceField(
        choices=[
            ('Muy dispuesto', 'Muy dispuesto'),
            ('Moderadamente dispuesto', 'Moderadamente dispuesto'),
            ('Prefiero evitarlo', 'Prefiero evitarlo'),
        ],
        label="4. ¿Qué tan dispuesto estás a asumir los costos de cuidados específicos como alimento especializado o tratamientos médicos frecuentes?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(4)"})

    )

    # Pregunta 5: ¿Qué tan tolerante eres con comportamientos como arañar muebles o maullar frecuentemente?
    tolerante = forms.ChoiceField(
        choices=[
            ('Muy tolerante', 'Muy tolerante'),
            ('Moderadamente tolerante', 'Moderadamente tolerante'),
            ('Poco tolerante', 'Poco tolerante'),
        ],
        label="5. ¿Qué tan tolerante eres con comportamientos como arañar muebles o maullar frecuentemente?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(5)"})

    )

    # Continuar de manera similar con las demás preguntas...
    vivienda = forms.ChoiceField(
        choices=[
            ('Casa con jardín o terraza', 'Casa con jardín o terraza'),
            ('Apartamento pequeño', 'Apartamento pequeño'),
            ('Apartamento grande', 'Apartamento grande'),
        ],
        label="6. ¿Dónde vives actualmente?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(6)"})

    )

    espacio_especifico = forms.ChoiceField(
        choices=[
            ('Sí, totalmente dispuesto', 'Sí, totalmente dispuesto'),
            ('Sí, pero con limitaciones', 'Sí, pero con limitaciones'),
            ('No', 'No'),
        ],
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(7)"})

    )

    exterior_interior = forms.ChoiceField(
        choices=[
            ('Exterior', 'Exterior'),
            ('Interior', 'Interior'),
            ('Ambos', 'Ambos'),
        ],
        label="8. ¿Prefieres un gato que pueda salir al exterior o que sea exclusivamente de interior?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(8)"})

    )

    adaptacion = forms.ChoiceField(
        choices=[
            ('Sí, completamente dispuesto', 'Sí, completamente dispuesto'),
            ('Moderadamente dispuesto', 'Moderadamente dispuesto'),
            ('No estoy seguro', 'No estoy seguro'),
            ('Subjetivas o psicológicas', 'Subjetivas o psicológicas'),
        ],
        label="9. ¿Estás dispuesto a lidiar con periodos de adaptación si el gato es tímido o reservado al principio?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(9)"})
    )

    porque_adoptar = forms.ChoiceField(
        choices=[
            ('Compañía emocional', 'Compañía emocional'),
            ('Ayudar a un animal que lo necesita', 'Ayudar a un animal que lo necesita'),
            ('Tener una presencia tranquila en casa', 'Tener una presencia tranquila en casa'),
            ('Otros', 'Otros'),
        ],
        label="10. ¿Por qué quieres adoptar un gato?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(10)"})

    )

    situacionesImprevistas = forms.ChoiceField(
        choices=[
            ('Me adapto fácilmente', 'Me adapto fácilmente'),
            ('Me cuesta pero intento resolverlo', 'Me cuesta pero intento resolverlo'),
            ('Prefiero evitar complicaciones', 'Prefiero evitar complicaciones'),
        ],
        label="11. ¿Cómo manejas situaciones estresantes o imprevistas con una mascota?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(11)"})

    )

    cariñoso = forms.ChoiceField(
        choices=[
            ('Muy importante', 'Muy importante'),
            ('Moderadamente importante', 'Moderadamente importante'),
            ('Poco importante', 'Poco importante'),
        ],
        label="12. ¿Qué tan importante es para ti que el gato sea cariñoso contigo?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(12)"})

    )

    enriquecer = forms.ChoiceField(
        choices=[
            ('Reduciendo el estrés', 'Reduciendo el estrés'),
            ('Proporcionando compañía', 'Proporcionando compañía'),
            ('Como un nuevo pasatiempo o responsabilidad', 'Como un nuevo pasatiempo o responsabilidad'),
        ],
        label="13. ¿Cómo crees que un gato puede enriquecer tu vida?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(13)"})

    )

    conexion_emocional = forms.ChoiceField(
        choices=[
            ('Un vínculo cercano y constante', 'Un vínculo cercano y constante'),
            ('Una relación tranquila pero no muy intensa', 'Una relación tranquila pero no muy intensa'),
            ('Independencia mutua', 'Independencia mutua'),
        ],
        label="14. ¿Qué tipo de conexión emocional esperas tener con el gato?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(14)"})

    )

    que_valoras = forms.ChoiceField(
        choices=[
            ('Su carácter y personalidad', 'Su carácter y personalidad'),
            ('Su apariencia física', 'Su apariencia física'),
            ('Su capacidad de adaptarse a mi estilo de vida', 'Su capacidad de adaptarse a mi estilo de vida'),
        ],
        label="15. ¿Qué valoras más en una mascota?",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "handleChange(15)"})

    )

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