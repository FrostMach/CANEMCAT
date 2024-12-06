from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm,AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser, Wishlist
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.core.files.storage import default_storage
import tensorflow as tf
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import smtplib
from django.http import HttpResponse
import requests
from django.utils.encoding import force_bytes
from django.http import JsonResponse
from shelters.models import Animal
import numpy as np

def landing_page(request):
    return render(request, 'landing_page.html')

#CANEMSCAN
from django.http import JsonResponse
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os

# Ruta al modelo entrenado
MODEL_PATH = os.path.join(settings.BASE_DIR, 'Users', 'IA', 'CanemSCAN2000.h5')
model = load_model(MODEL_PATH)

# Lista de razas en el orden del modelo
BREEDS = ['Affenpinscher', 'American Staffordshire Terrier', 'Basenji', 'Basset Hound', 'Beagle', 'Bedlington Terrier', 'Bichón maltés', 'Black and Tan Coonhound', 'Bluetick Coonhound', 'Bobtail', 'Border Collie', 'Border Terrier', 'Borzoi', 'Boston Terrier', 'Boxer', 'Boyer de Entlebuch', 'Boyero de Appenzell', 'Boyero de Berna', 'Boyero de Flandes', 'Braco alemán de pelo corto', 'Braco de Weimar', 'Bulldog francés', 'Bullmastiff', 'Cairn Terrier', 'Caniche enano', 'Cavalier King Charles Spaniel', 'Cazador de alces noruego', 'Chihuahua', 'Chin japonés', 'Chow Chow', 'Clumber Spaniel', 'Cobrador de pelo liso', 'Cocker inglés', 'Collie', 'Corgi galés de Cardigan', 'Corgi galés de Pembroke', 'Cuon alpinus', 'Dachshund', 'Dandie Dinmont Terrier', 'Dingo', 'Doberman', 'Dogo del Tíbet', 'Dálmata', 'Esquimal americano', 'Fox Terrier de pelo duro', 'Foxhound inglés', 'Galgo italiano', 'Golden Retriever', 'Gordon Setter', 'Gran boyer suizo', 'Gran danés', 'Husky siberiano', 'Keeshond', 'Kelpie australiano', 'Kerry Blue Terrier', 'Komondor', 'Kuvasz húngaro', 'Labrador Retriever', 'Lakeland Terrier', 'Lebrel afgano', 'Lebrel escocés', 'Leonberger', 'Lhasa Apso', 'Lobero irlandés', 'Malamute de Alaska', 'Otterhound', 'Papillón', 'Pastor alemán', 'Pastor belga Groenendael', 'Pastor belga Malinois', 'Pastor de Brie', 'Pastor de islas Shetland', 'Pekinés', 'Perro crestado rodesiano', 'Perro de agua irlandés', 'Perro de montaña de los Pirineos', 'Perro de San Huberto', 'Perro salvaje africano', 'Petit Brabançon', 'Pinscher miniatura', 'Podenco ibicenco', 'Pomeranian', 'Poodle estándar', 'Poodle Toy', 'Pug', 'Redbone Coonhound', 'Retriever de Chesapeake', 'Retriever de pelo rizado', 'Rottweiler', 'Saluki', 'Samoyedo', 'San Bernardo', 'Schipperke', 'Schnauzer estándar', 'Schnauzer gigante', 'Schnauzer miniatura', 'Sealyham Terrier', 'Setter inglés', 'Setter irlandés', 'Shiba Inu', 'Shih Tzu', 'Silky Terrier australiano', 'Soft Coated Wheaten Terrier', 'Spaniel Bretón', 'Springer spaniel galés', 'Springer Spaniel inglés', 'Staffordshire Bull Terrier', 'Sussex Spaniel', 'Terranova', 'Terrier de Airedale', 'Terrier de Australia', 'Terrier de Norfolk', 'Terrier de Norwich', 'Terrier escocés', 'Terrier irlandés', 'Terrier tibetano', 'Toy Terrier inglés', 'Treeing Walker Coonhound', 'Vizsla', 'West Highland White Terrier', 'Whippet', 'Xoloitzcuintle', 'Yorkshire Terrier']  # Actualiza según tu entrenamiento

def canem_scan(request):
    return render(request, 'canemscan.html')

def upload_image(request):
    if request.method == 'POST' and 'image' in request.FILES:
        uploaded_file = request.FILES['image']

        # Guardar temporalmente la imagen
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded')
        os.makedirs(upload_dir, exist_ok=True)
        saved_path = os.path.join(upload_dir, uploaded_file.name)

        with open(saved_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        try:
            # Preprocesar la imagen
            img = load_img(saved_path, target_size=(224, 224))  # Tamaño esperado por el modelo
            img_array = img_to_array(img) / 255.0  # Normalización
            img_array = img_array.reshape((1, 224, 224, 3))  # Asegurar las dimensiones correctas

            # Realizar predicción
            predictions = model.predict(img_array)  # Devuelve probabilidades
            predicted_index = predictions.argmax()  # Índice de la probabilidad más alta
            predicted_breed = BREEDS[predicted_index]  # Obtener la raza correspondiente

            # Guardar la raza detectada en la sesión
            request.session['detected_breed'] = predicted_breed

            image_url = f"/media/uploaded/{uploaded_file.name}"

            # Devolver la predicción como JSON
            return JsonResponse({'image_url': image_url, 'breed': f"La raza detectada es: {predicted_breed}"})

        except Exception as e:
            os.remove(saved_path) 
            return JsonResponse({'error': f'Ocurrió un error al procesar la imagen: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método no permitido o archivo no recibido'}, status=400)



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
        form = AuthenticationForm(request, data=request.POST)  # Necesitamos pasar `request` al form

        email = request.POST.get('email')
        password = request.POST.get('password')

        # Intentamos obtener el usuario con el email
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None

        # Si el usuario existe, intentamos autenticarlo
        if user is not None:
            user = authenticate(request, email=user.email, password=password)  # Usamos el username para la autenticación
            if user is None:
                form.add_error(None, "Email o contraseña incorrectos")  # Agregar un error general al formulario
            else:
                login(request, user)  # Iniciar sesión si la autenticación es exitosa
                return redirect('landing_page')  # Redirige a la página principal o dashboard
        else:
            form.add_error(None, "Usuario con ese email no encontrado.")  # Agregar un error si no se encuentra el usuario
        
    else:
        form = AuthenticationForm()

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

def send_mail(to, subject, body, from_mail="pruebasconsmtp46@gmail.com", password="mmxl tlnu lxpt rvjr"):
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

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            users = CustomUser.objects.filter(email=email)  # Aquí buscamos todos los usuarios con ese email
            
            # Si hay al menos un usuario con el email, tomamos el primero
            if users.exists():
                user = users.first()  # Tomamos el primer usuario
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk.to_bytes()))  # Usamos force_bytes para convertir el ID a bytes
                current_site = get_current_site(request)
                mail_subject = 'Enlace para recuperar la contraseña'
                message = render_to_string('registration/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                })
                send_mail(mail_subject, message, 'from@example.com', [email])  # Reemplaza 'from@example.com' con tu correo
                return render(request, 'registration/password_reset_done.html')  # Redirige a la página de confirmación
            else:
                # Si no se encuentra un usuario con ese email
                form.add_error('email', 'No se ha encontrado ningún usuario con ese correo electrónico.')
    else:
        form = PasswordResetForm()

    return render(request, 'registration/password_reset.html', {'form': form})

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