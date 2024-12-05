from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import views as auth_views
from .forms import CustomUserCreationForm, CustomUserChangeForm,AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser, Wishlist,Test,CompatibilityTest
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import smtplib
from django.http import HttpResponse
import requests
from django.utils.encoding import force_bytes
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.conf import settings

@never_cache
def landing_page(request):
    print(f"Usuario autenticado en landing: {request.user.is_authenticated}")
    print(f"Sesión en landing: {request.session.items()}")
    return render(request, 'landing_page.html')

#USUARIOS

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

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
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            logout(request)  # Cerrar sesión antes de iniciar sesión
            login(request, user)
            print(f"Usuario autenticado en login (después de login): {request.user.is_authenticated}")
            print(f"Sesión en login: {request.session.items()}")
            return HttpResponseRedirect(reverse('landing_page'))  # o 'landing_page' si tienes nombre de ruta para la landing
        else:
            messages.error(request, "Email o contraseña incorrectos.")
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # El usuario no estará activo hasta que confirme su email
            user.save()

            # # Enviar correo de confirmación
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(user.pk.to_bytes())
            current_site = get_current_site(request)
            mail_subject = 'Confirma tu correo electrónico'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(user.email,mail_subject, message)

            return render(request,'registration/email_confirmation.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def send_mail(to, subject, body, from_mail=settings.DEFAULT_FROM_EMAIL, password=settings.EMAIL_HOST_PASS):
    from email.mime.text import MIMEText
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_mail
    msg['To'] = to
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_mail, password)
    s.sendmail(from_mail, [to], msg.as_string())
    s.quit()


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset.html'  # Plantilla personalizada para el formulario
    email_template_name = 'registration/password_reset_email.html'  # Plantilla personalizada para el correo
    subject_template_name = 'registration/password_reset_subject.txt'  # Plantilla personalizada para el asunto
    success_url = reverse_lazy('password_reset_done')  # Redirige a la vista de "Correo Enviado"

    def get_users(self, email):
        """
        Sobrescribe el método `get_users` para devolver el queryset de usuarios
        que coinciden con el correo electrónico proporcionado.
        """
        from django.contrib.auth.models import User
        return CustomUser.objects.filter(email=email)

    def form_valid(self, form):
        """
        Sobrescribir el método para manejar el formulario válido y enviar el correo.
        """
        email = form.cleaned_data['email']

        # Obtener el queryset de usuarios con el correo proporcionado usando get_users()
        users = self.get_users(email)

        # Si no hay usuarios con ese correo, no hacemos nada
        if not users:
            return self.render_to_response(self.get_context_data(form=form))

        # Si hay usuarios, generamos el correo para cada uno
        for user in users:
            # Crear el token y el UID
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))

            # Preparar el mensaje del correo
            subject = render_to_string(self.subject_template_name, {'user': user})
            subject = ''.join(subject.splitlines())

            message = render_to_string(self.email_template_name, {
                'user': user,
                'domain': get_current_site(self.request).domain,
                'site_name': get_current_site(self.request).name,
                'uid': uid,
                'token': token,
                'protocol': 'https' if self.request.is_secure() else 'http',
            })

            # Enviar el correo
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )

        return super().form_valid(form)

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'  

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'  
    success_url = reverse_lazy('password_reset_complete')  

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'  # Personaliza la plantilla si lo deseas

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


    
class DogTestView(generic.ListView):
    model = Test
    template_name = 'test/dog_test.html'

class CatTestView(generic.ListView):
    model = Test
    template_name = 'test/cat_test.html'

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
        return redirect('login')  # O hacia la página de login
    return render(request, 'test/canemtest.html')


def test_compatibilidad(request):
    if request.method == "POST":
        # Obtener las respuestas del formulario
        respuesta = {
            'tamaño': request.POST['tamaño'],
            'edad': request.POST['edad'],
            'energia': request.POST['energia'],
            'pelaje': request.POST['pelaje'],
            'caracter': request.POST['caracter'],
            'paseo': request.POST['paseo'],
            'frecuencia_casa': request.POST['frecuenciaCasa'],
            'familia': request.POST['familia'],
            'otras_mascotas': request.POST['otrasMascotas'],
            'vivienda': request.POST['vivienda'],
            'entrenamiento': request.POST['entrenamiento'],
            'bienestar_emocional': request.POST['bienestarEmocional'],
            'razon_adopcion': request.POST['razonAdopcion'],
            'situaciones_imprevistas': request.POST['situacionesImprevistas'],
            'paciencia': request.POST['paciencia'],
            'problema_comportamiento': request.POST['problemaComportamiento'],
            'convivencia_externa': request.POST['convivenciaExterna'],
            'cuidados_medicos': request.POST['cuidadosMedicos'],
            'conexion_emocional': request.POST['conexionEmocional'],
            'actividad_cotidiana': request.POST['actividadCotidiana'],
        }

        # Guardar respuestas en el modelo CompatibilityTest
        test = CompatibilityTest.objects.create(
            user=request.user,  # Si deseas asociar el test a un usuario
            **respuesta
        )

        # Filtrar animales según las preferencias
        animales = "shelters.Animal".objects.filter(
            size__icontains=respuesta['tamaño'],
            age__gte=5,  # Por ejemplo, si la edad preferida es "joven" o "adulto"
            energy__icontains=respuesta['energia'],
            fur__icontains=respuesta['pelaje'],
            personality__icontains=respuesta['caracter'],
            adoption_status="disponible"
        )

        # Ajustar el filtro de animales basado en las respuestas (esto es un ejemplo básico)
        if respuesta['actividad_cotidiana'] == 'Activa':
            animales = animales.filter(energy="activo")

        return render(request, 'resultado_adopcion.html', {'animales': animales})

    return render(request, 'test_adopcion.html')



