from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

# Este formulario ya está incluido en Django, solo necesitas importarlo.
from django import forms
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

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'phone_number', 'birth_date', 'profile_picture', 'user_type')
        

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Guardamos el request
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        print(f"Cleaning form: email={email}, password={password}")  # Depuración

        if email and password:
            # Usamos authenticate, asegurándonos de pasar el 'email'
            user = authenticate(request=self.request, username=email, password=password)  # 'username' es 'email' aquí
            print(f"Authenticate result: {user}")  # Depuración para ver si la autenticación falla
            if user is None:
                raise forms.ValidationError("Email o contraseña incorrectos.")
            self.user = user
        return self.cleaned_data