from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import views as auth_views
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Wishlist,Test
from django.contrib.auth import login, logout, get_user_model
from .forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import smtplib
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.conf import settings
from .forms import TestPerroForm, TestGatoForm
from .utils import encontrar_animal_ideal
from shelters.models import Animal
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
def canem_test(request):
    if request.method == 'POST':
        especie = request.POST.get('especie')  # Recoge la especie seleccionada
        
        if not especie:
            # Si no se seleccionó ninguna opción, puedes mostrar un error o redirigir a otra página
            return render(request, 'test/canem_test.html', {'error': 'Por favor selecciona una especie.'})
        
        if especie == 'Perro':
            return redirect('dog_test')  # Redirige al test de perros (usa el nombre de la URL correspondiente)
        elif especie == 'Gato':
            return redirect('cat_test')  # Redirige al test de gatos (usa el nombre de la URL correspondiente)
        else:
            return render(request, 'test/canem_test.html', {'error': 'Especie no válida.'})
    
    # Si el método no es POST, simplemente muestra el formulario
    return render(request, 'test/canem_test.html')

def test_perro(request):
    if request.method == 'POST':
        form = TestPerroForm(request.POST)
        especie = 'perro' 
        if form.is_valid():
            respuestas = form.cleaned_data
            # Buscamos el perro ideal
            animal_ideal = encontrar_animal_ideal(respuestas, 'perro')
            return render(request, 'test/adoption_result.html', {'animal_ideal': animal_ideal, 'especie': especie})
    else:
        form = TestPerroForm()
    return render(request, 'dog_test.html', {'form': form, 'especie': especie})

def test_gato(request):
    if request.method == 'POST':
        form = TestGatoForm(request.POST)
        especie = 'gato' 
        if form.is_valid():
            respuestas = form.cleaned_data
            # Buscamos el gato ideal
            animal_ideal = encontrar_animal_ideal(respuestas, 'gato')
            return render(request, 'test/adoption_result.html', {'animal_ideal': animal_ideal, 'especie': especie})
    else:
        form = TestGatoForm()
    return render(request, 'cat_test.html', {'form': form, 'especie': especie})

def resultado_test(request):
    # Verificar si el formulario fue enviado
    if request.method == "POST":
        # Obtener las respuestas del formulario y guardarlas en la sesión
        respuestas = {
            'tamano': request.POST.get('tamaño'),
            'edad': request.POST.get('edad'),
            'energia': request.POST.get('energia'),
            'pelaje': request.POST.get('pelaje'),
            'caracter': request.POST.get('caracter'),
            'paseo': request.POST.get('paseo'),
            'frecuenciaCasa': request.POST.get('frecuenciaCasa'),
            'familia': request.POST.get('familia'),
            'otrasMascotas': request.POST.get('otrasMascotas'),
            'vivienda': request.POST.get('vivienda'),
            'entrenamiento': request.POST.get('entrenamiento'),
            'bienestarEmocional': request.POST.get('bienestarEmocional'),
            'razonAdopcion': request.POST.get('razonAdopcion'),
            'situacionesImprevistas': request.POST.get('situacionesImprevistas'),
            'paciencia': request.POST.get('paciencia'),
            'problemaComportamiento': request.POST.get('problemaComportamiento'),
            'convivenciaExterna': request.POST.get('convivenciaExterna'),
            'cuidadosMedicos': request.POST.get('cuidadosMedicos'),
            'conexionEmocional': request.POST.get('conexionEmocional'),
            'actividadCotidiana': request.POST.get('actividadCotidiana')
        }
        # Guardar las respuestas en la sesión
        request.session['respuestas'] = respuestas
        # Obtener la especie de la respuesta (supongamos que se tiene una pregunta para esto)
        especie = request.POST.get('especie')  # Esta respuesta debería venir de alguna parte
        print(f"la especie es: {especie}")
        # Verificar que la especie sea válida y crear el formulario correspondiente
        if especie == 'perro':
            form = TestPerroForm(respuestas)
        elif especie == 'gato':
            form = TestGatoForm(respuestas)
        else:
            return render(request, 'error.html', {'mensaje': 'Especie no válida.'})
        
        # Filtrar los animales por especie
        animales = Animal.objects.filter(species=especie)

        # Crear una lista para almacenar las puntuaciones de compatibilidad
        puntuaciones = []
        
        # Iterar sobre los animales
        for animal in animales:
            puntuacion = 0

            # Comparar las respuestas con las características del animal
            if animal.personality == respuestas.get('caracter'):
                puntuacion += 1
            if animal.size == respuestas.get('tamano'):
                puntuacion += 1
            if animal.energy == respuestas.get('energia'):
                puntuacion += 1
            # Se pueden agregar más comparaciones aquí

            puntuaciones.append({'animal': animal, 'puntuacion': puntuacion})

        # Ordenar los animales por puntuación
        puntuaciones = sorted(puntuaciones, key=lambda x: x['puntuacion'], reverse=True)
        print(f"puntuaciones ssss: {puntuaciones}")

        # Seleccionar el animal con la mayor puntuación
        if puntuaciones:
            animal_ideal = puntuaciones[0]['animal']
        else:
            animal_ideal = None

        # Mostrar el resultado
        return render(request, 'test/adoption_result.html', {
            'animal_ideal': animal_ideal,
            'especie': especie,
        })

    else:
        return render(request, 'error.html', {'mensaje': 'No se han recibido respuestas.'})