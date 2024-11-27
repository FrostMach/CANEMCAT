from django.shortcuts import render, redirect,redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Wishlist
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
import requests

def landing_page(request):
    return render(request, 'landing_page.html')

#USUARIOS

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # El usuario no estará activo hasta que confirme su email
            user.save()

            # Enviar correo de confirmación
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            current_site = get_current_site(request)
            mail_subject = 'Confirma tu correo electrónico'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, 'pruebaconsmtp46@gmail.com', [user.email])

            return redirect('registration/email_confirmation.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_registration_view(request):
    if request.method == "POST":

        subject = "Bienvenido a nuestro sitio"
        body = "Gracias por registrarte. Estamos emocionados de tenerte con nosotros."
        to_email = "user@example.com"  
        
        send_mail(subject, body, to_email)

        return HttpResponse("Registro completado y correo enviado.")
    
    return render(request, 'signup.html')


def email_confirmation(request):
    return render(request, 'registration/email_confirmation.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('registration/login.html')
        else:
            messages.error(request, "El enlace de activación es inválido o ha expirado.")
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        messages.error(request, "El enlace de activación es inválido.")
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('landing_page')  # Redirigir al home u otra página
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            users = CustomUser.objects.filter(email=email)
            for user in users:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode())
                current_site = get_current_site(request)
                mail_subject = 'Recupera tu contraseña'
                message = render_to_string('registration/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                })
                send_mail(mail_subject, message, 'pruebasconsmtp46@gmail.com', [email])
            return redirect('password_reset_confirm')
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset.html', {'form': form})

class ProfileView(generic.DetailView):
    model = CustomUser
    template_name = 'profile.html'

class ProfileUpdateView(generic.UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('profile')
    

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing_page')  # Redirigir a la página principal o a la página de perfil
        else:
            # Si el inicio de sesión es incorrecto, muestra un mensaje de error
            return render(request, 'registration/login.html', {'error': 'Correo o contraseña incorrectos'})

    return render(request, 'registration/login.html')


# def signup_view(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Iniciar sesión automáticamente
#             return redirect('landing_page')  # Redirigir a la página principal o perfil
#     else:
#         form = UserCreationForm()

#     return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing_page')    
#WISHLIST    

class AddToWishlistView(generic.ListView):
    
    model = Wishlist
    template_name = 'wish/list.html'
    context_object_name = 'add'

class RemoveFromWishlistView(generic.ListView):
    
    model = Wishlist
    template_name = 'wish/list.html'
    context_object_name = 'remove'


from django.contrib.auth.decorators import login_required

@login_required
def canemscan_view(request):
    if request.user.user_type != 'adopter':
        # Si no es un 'adopter', redirigimos a una página de acceso denegado o algo similar
        return redirect('access_denied')  # Puedes crear una página para mostrar acceso denegado
    return render(request, 'canemscan.html')

@login_required
def canemtest_view(request):
    if request.user.user_type != 'adopter':
        # Redirigir a una página de acceso denegado
        return redirect('access_denied')  # O hacia la página de login
    return render(request, 'canemtest.html')
