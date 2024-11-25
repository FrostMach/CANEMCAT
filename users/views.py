from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate,get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Wishlist
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
            send_mail(mail_subject, message, 'no-reply@example.com', [user.email])

            return redirect('registration/email_confirmation.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def send_mailgun_email(subject, body, to_email):
    api_key = "c62cd9774f0f4cb5a055e4b8e4c7e81f-6df690bb-ebd2b32a"
    domain = "sandbox47fab76e50d34c02b56708c10cf6c76f.mailgun.org"
    from_email = "pruebasconsmtp46@gmail.com"

    response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": from_email,
            "to": to_email,
            "subject": subject,
            "text": body
        }
    )

    return response

def user_registration_view(request):
    if request.method == "POST":

        subject = "Bienvenido a nuestro sitio"
        body = "Gracias por registrarte. Estamos emocionados de tenerte con nosotros."
        to_email = "user@example.com"  
        
        send_mailgun_email(subject, body, to_email)

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
                send_mail(mail_subject, message, 'no-reply@example.com', [email])
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
    
    
#WISHLIST    

class AddToWishlistView(generic.ListView):
    
    model = Wishlist
    template_name = 'wish/list.html'
    context_object_name = 'add'

class RemoveFromWishlistView(generic.ListView):
    
    model = Wishlist
    template_name = 'wish/list.html'
    context_object_name = 'remove'


