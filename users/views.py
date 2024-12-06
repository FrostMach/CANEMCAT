from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth import views as auth_views
from shelters.models import Animal
# from sys_recommend.sys_recommend import recommend_pets
from .forms import CustomUserCreationForm, CustomUserChangeForm,AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser, Wishlist, Test, AdopterProfile
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import LoginForm
from django.shortcuts import render
from django.core.files.storage import default_storage
import tensorflow as tf
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import smtplib
import requests
from django.utils.encoding import force_bytes
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from .forms import TestPerroForm, TestGatoForm
from .utils import encontrar_animal_ideal
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import csv

@never_cache

def landing_page(request):
    print(f"Usuario autenticado en landing: {request.user.is_authenticated}")
    print(f"Sesión en landing: {request.session.items()}")
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
@login_required    
def wishlist_add(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    if request.method == 'POST':
        interaction_type = request.POST.get('interaction_type')
        Wishlist.objects.get_or_create(user=request.user, animal=animal, interaction_type=interaction_type)
        return redirect('wishlist_list')
    return render(request, 'add_to_wishlist.html', {'animal': animal})

@login_required
def wishlist_remove(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist_list')

@login_required
def wishlist_list(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wish/list.html', {'wishlist_items': wishlist_items})


    
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
        return redirect('access_denied')  # O hacia la página de login
    return render(request, 'canemtest.html')

def test_perro(request):
    if request.method == 'POST':
        form = TestPerroForm(request.POST)
        if form.is_valid():
            respuestas = form.cleaned_data
            # Buscamos el perro ideal
            animal_ideal = encontrar_animal_ideal(respuestas, 'perro')
            return render(request, 'resultado_test.html', {'animal_ideal': animal_ideal, 'especie': 'Perro'})
    else:
        form = TestPerroForm()
    return render(request, 'test_perro.html', {'form': form})

def test_gato(request):
    if request.method == 'POST':
        form = TestGatoForm(request.POST)
        if form.is_valid():
            respuestas = form.cleaned_data
            # Buscamos el gato ideal
            animal_ideal = encontrar_animal_ideal(respuestas, 'gato')
            return render(request, 'resultado_test.html', {'animal_ideal': animal_ideal, 'especie': 'Gato'})
    else:
        form = TestGatoForm()
    return render(request, 'test_gato.html', {'form': form})

def resultado_test(request):
    # Obtener las respuestas del usuario desde la sesión (o el método que uses)
    respuestas = request.session.get('respuestas_test', None)

    if not respuestas:
        return render(request, 'error.html', {'mensaje': 'No se han encontrado respuestas para el test.'})
    
    especie = respuestas.get('especie', None)  # 'perro' o 'gato'
    if especie == 'perro':
        form = TestPerroForm(respuestas)
    elif especie == 'gato':
        form = TestGatoForm(respuestas)
    else:
        return render(request, 'error.html', {'mensaje': 'Especie no válida.'})

    # Filtrar los animales por especie (perro o gato)
    animales = "shelters.Animal".objects.filter(species=especie)

    # Crear una lista para almacenar la puntuación de compatibilidad de cada animal
    puntuaciones = []

    # Iterar a través de todos los animales filtrados
    for animal in animales:
        puntuacion = 0

        # Comparar las respuestas del usuario con las características del animal
        # Puntuación por personalidad
        if animal.personality == respuestas.get('personalidad'):
            puntuacion += 1  # Añadimos un punto por cada coincidencia

        # Puntuación por tamaño
        if animal.size == respuestas.get('tamano'):
            puntuacion += 1

        # Puntuación por energía
        if animal.energy == respuestas.get('energia'):
            puntuacion += 1

        # Puedes añadir más criterios aquí según sea necesario

        # Añadir el animal y su puntuación a la lista
        puntuaciones.append({'animal': animal, 'puntuacion': puntuacion})

    # Ordenar los animales por puntuación en orden descendente
    puntuaciones = sorted(puntuaciones, key=lambda x: x['puntuacion'], reverse=True)

    # Seleccionar el animal con la mayor puntuación (el más compatible)
    if puntuaciones:
        animal_ideal = puntuaciones[0]['animal']
    else:
        animal_ideal = None

    # Pasar el resultado a la plantilla
    return render(request, 'resultado_test.html', {
        'animal_ideal': animal_ideal,
        'especie': especie,
    })
    
def admin_only(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(admin_only)
def export_animals_csv(request):
    animals = Animal.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="animals.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Age', 'Species', 'Description', 'Image', 'Adoption_status'])

    for animal in animals:
        writer.writerow([animal.id, animal.name, animal.age, animal.species, animal.description, animal.image, animal.adoption_status])

    return response

@user_passes_test(admin_only)
def export_interactions_csv(request):
    interactions = Wishlist.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="interactions.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'User', 'Animals', 'Interaction_type'])

    for interaction in interactions:
        writer.writerow([interaction.id, interaction.user, interaction.animals, interaction.interaction_type])
    
    return response

# def dashboard_recommendations(request):
#     user_id = request.user.id

#     recommendations = recommend_pets(user_id)

#     recommendations_list = recommendations.to_dict('records') if not recommendations.empty else []

#     return render(request, 'recommend/list.html', {'recommendations':recommendations_list})

# def record_interaction(request, animal_id, interaction_type):
#     if request.method == 'POST':
#         user = request.user
#         animal = get_object_or_404(Animal, id=animal_id)

#         interaction = Wishlist.object.create(user=user, animal=animal, interaction_type=interaction_type)

#         return JsonResponse({
#             'message': 'Interacción registrada exitosamente'
#         })
    
#     return JsonResponse({
#         'error': 'Método no permitido'
#     }, status=405)    