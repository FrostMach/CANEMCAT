import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth import views as auth_views
from shelters.models import Animal
from users.sys_recommend.sys_recommend import get_user_recommendations
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
from shelters.models import Animal
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import csv
import os

@never_cache
def landing_page(request):
    animals = Animal.objects.filter(adoption_status='Disponible')
    return render(request, 'landing_page.html', {'animals': animals})

#CANEMSCAN
from django.http import JsonResponse
from django.conf import settings
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
import numpy as np

# Ruta al modelo entrenado
MODEL_PATH = os.path.join(settings.BASE_DIR, 'Users', 'IA', 'CanemSCAN2200.h5')
model = load_model(MODEL_PATH)

# Lista de razas en el orden del modelo
BREEDS = ['Affenpinscher', 'American Staffordshire Terrier', 'Basenji', 'Basset Hound', 'Beagle', 'Bedlington Terrier', 'Bichón maltés', 'Black and Tan Coonhound', 'Bluetick Coonhound', 'Bobtail', 'Border Collie', 'Border Terrier', 'Borzoi', 'Boston Terrier', 'Boxer', 'Boyer de Entlebuch', 'Boyero de Appenzell', 'Boyero de Berna', 'Boyero de Flandes', 'Braco alemán de pelo corto', 'Braco de Weimar', 'Bull Terrier', 'Bulldog francés', 'Bullmastiff','Cairn Terrier', 'Caniche enano', 'Cavalier King Charles Spaniel', 'Cazador de alces noruego', 'Chihuahua', 'Chin japonés', 'Chow Chow', 'Clumber Spaniel', 'Cobrador de pelo liso', 'Cocker inglés', 'Collie', 'Corgi galés de Cardigan', 'Corgi galés de Pembroke', 'Cuon alpinus', 'Dachshund', 'Dandie Dinmont Terrier', 'Dingo', 'Doberman', 'Dogo del Tíbet', 'Dálmata', 'Esquimal americano', 'Fox Terrier de pelo duro', 'Foxhound inglés', 'Galgo italiano', 'Golden Retriever', 'Gordon Setter', 'Gran boyer suizo', 'Gran danés', 'Husky siberiano', 'Keeshond', 'Kelpie australiano', 'Kerry Blue Terrier', 'Komondor', 'Kuvasz húngaro', 'Labrador Retriever', 'Lakeland Terrier', 'Lebrel afgano', 'Lebrel escocés', 'Leonberger', 'Lhasa Apso', 'Lobero irlandés', 'Malamute de Alaska', 'Otterhound', 'Papillón', 'Pastor alemán', 'Pastor belga Groenendael', 'Pastor belga Malinois', 'Pastor de Brie', 'Pastor de islas Shetland', 'Pekinés', 'Perro crestado rodesiano', 'Perro de agua irlandés', 'Perro de montaña de los Pirineos', 'Perro de San Huberto', 'Perro salvaje africano', 'Petit Brabançon', 'Pinscher miniatura', 'Podenco ibicenco', 'Pomeranian', 'Poodle estándar', 'Poodle Toy', 'Pug', 'Redbone Coonhound', 'Retriever de Chesapeake', 'Retriever de pelo rizado', 'Rottweiler', 'Saluki', 'Samoyedo', 'San Bernardo', 'Schipperke', 'Schnauzer estándar', 'Schnauzer gigante', 'Schnauzer miniatura', 'Sealyham Terrier', 'Setter inglés', 'Setter irlandés', 'Shiba Inu', 'Shih Tzu', 'Silky Terrier australiano', 'Soft Coated Wheaten Terrier', 'Spaniel Bretón', 'Springer spaniel galés', 'Springer Spaniel inglés', 'Staffordshire Bull Terrier', 'Sussex Spaniel', 'Terranova', 'Terrier de Airedale', 'Terrier de Australia', 'Terrier de Norfolk', 'Terrier de Norwich', 'Terrier escocés', 'Terrier irlandés', 'Terrier tibetano', 'Toy Terrier inglés', 'Treeing Walker Coonhound', 'Vizsla', 'West Highland White Terrier', 'Whippet', 'Xoloitzcuintle', 'Yorkshire Terrier']  # Actualiza según tu entrenamiento

#EXTRACTOR DE VECTORES DE IMÁGENES
feature_extractor = Model(inputs=model.input, outputs=model.layers[-2].output)

def extract_features(image_path):
    """
    Extrae un vector de características de una imagen usando el modelo preentrenado.
    """
    img = load_img(image_path, target_size=(224, 224))  # Redimensionar la imagen
    img_array = img_to_array(img) / 255.0  # Normalizar
    img_array = img_array.reshape((1, 224, 224, 3))  # Añadir dimensión batch
    features = feature_extractor.predict(img_array)  # Extraer características
    return features.flatten()  # Devolver como un vector 1D

#OBTENER IMÁGENES Y CARACTERÍSTICAS DE LA BASE DE DATOS

def get_animal_images_and_features():
    """
    Recupera las rutas de las imágenes de los perros en la base de datos
    y extrae sus características.
    """
    animals = Animal.objects.filter(species='perro')  # Filtrar solo perros
    images_and_features = []
    
    for animal in animals:
        image_path = animal.image.path  # Ruta de la imagen
        if os.path.exists(image_path):  # Comprobar que la imagen existe
            features = extract_features(image_path)  # Extraer características
            images_and_features.append((animal, features))
    
    return images_and_features  # Lista de tuplas (animal, características)


#COMPARADOR DE IMÁGENES
from scipy.spatial.distance import cosine

def find_similar_images(uploaded_image_path, animal_features, top_n=4):
    """
    Encuentra las imágenes más similares a la imagen cargada.
    """
    uploaded_features = extract_features(uploaded_image_path)  # Extraer características de la imagen subida
    similarities = []

    for animal, features in animal_features:
        similarity = 1 - cosine(uploaded_features, features)  # Similitud basada en el coseno
        similarities.append((animal, similarity))
    
    # Ordenar por similitud descendente
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    return similarities[:top_n]  # Devolver las N más similares

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
            
            image_id = uploaded_file.name

            # Guardar la raza detectada en la sesión
            request.session['detected_breed'] = predicted_breed
            image_url = f"/media/uploaded/{uploaded_file.name}"

            # Devolver la predicción como JSON
            return JsonResponse({'image_url': image_url, 'breed': f"La raza detectada es: {predicted_breed}", 'image_id': image_id})

        except Exception as e:
            os.remove(saved_path) 
            return JsonResponse({'error': f'Ocurrió un error al procesar la imagen: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método no permitido o archivo no recibido'}, status=400)

from django.urls import reverse

def compare_images(request):
    """
    Compara la imagen subida previamente con las de la base de datos.
    """
    # Recuperar el nombre del archivo subido desde la solicitud GET
    image_id = request.GET.get('uploaded_image_id', None)
    if not image_id:
        return JsonResponse({"error": "No se proporcionó el ID de la imagen."}, status=400)

    # Ruta a la imagen subida por el usuario
    uploaded_image_path = os.path.join(settings.MEDIA_ROOT, 'uploaded', image_id)
    if not os.path.exists(uploaded_image_path):
        return JsonResponse({'error': 'La imagen subida no se encuentra.'}, status=404)

    try:
        # Obtener características de las imágenes en la base de datos
        animal_features = get_animal_images_and_features()
        if not animal_features:
            return JsonResponse({"error": "No hay imágenes de animales en la base de datos para comparar."}, status=404)

        # Encontrar las imágenes más similares
        similar_images = find_similar_images(uploaded_image_path, animal_features)

        # Construir la respuesta con las imágenes más similares
        similar_results = [
            {
                'name': animal.name,
                'image_url': animal.image.url,
                'similarity': f'{similarity * 100:.2f}%',  # Convertir la similitud en porcentaje
                'detail_url': reverse('animals-detail', args=[animal.pk])  # Generar la URL de detalle
            }
            for animal, similarity in similar_images
        ]

        return JsonResponse({'similar_images': similar_results})

    except Exception as e:
        return JsonResponse({'error': f'Ocurrió un error al comparar las imágenes: {str(e)}'}, status=500)




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
    success_url = reverse_lazy('landing_page')

class ProfileWorkerView(generic.DetailView):
    model = CustomUser
    template_name = 'profile_worker.html'

class ProfileWorkerUpdateView(generic.UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'profile_worker_update.html'
    success_url = reverse_lazy('lab')


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
            uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
            token = default_token_generator.make_token(user)
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
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def get_users(self, email):
        return CustomUser.objects.filter(email=email)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        users = self.get_users(email)

        # Si no hay usuarios con el correo, no hacemos nada
        if not users:
            return self.render_to_response(self.get_context_data(form=form))

        # Procesar cada usuario encontrado
        for user in users:
            print(f"Procesando usuario: {user}")  # Imprimir el usuario completo para depuración

            # Verificar que `user.pk` no sea una lista ni otro tipo inesperado
            if isinstance(user.pk, list):
                print(f"Error: user.pk es una lista, valor: {user.pk}")
                return self.render_to_response(self.get_context_data(form=form))  # O manejar el error como sea necesario

            print(f"MAIL: {os.environ.get('MAIL')}")
            print(f"MAIL_PASSWORD: {os.environ.get('MAIL_PASSWORD')}")
            # Asegúrate de que `user.pk` es un valor correcto
            print(f"user pk: {user.pk}")  # Verificar el tipo y valor de `user.pk`
            # Usar `force_bytes` para convertir el ID a bytes
            uid = str(urlsafe_base64_encode(force_bytes(user.pk)))  # Asegúrate de que es una cadena
            print(f"UID generado: {uid}")  # Imprimir para verificar

            # Generar el token
            token = str(default_token_generator.make_token(user))  # Asegúrate de que es una cadena
            print(f"Token generado: {token}")  # Imprimir para verificar

            print(f"uid: {uid} (Tipo: {type(uid)})")
            print(f"token: {token} (Tipo: {type(token)})")
            print(f"email: {email} (Tipo: {type(email)})")
            # Preparar el asunto y el mensaje del correo
            subject = render_to_string(self.subject_template_name, {'user': user})
            subject = ''.join(subject.splitlines())

            message = render_to_string(self.email_template_name, {
                'user': user,
                'domain': get_current_site(self.request).domain,
                'site_name': get_current_site(self.request).name,
                'uid': str(uid),  # Asegúrate de que es una cadena
                'token': str(token), 
                'protocol': 'https' if self.request.is_secure() else 'http',
            })

            # Imprimir el email y su tipo para asegurarnos de que es una cadena
            print(f"Email: {email}")
            print(f"Valor de `email`: {email}")
            print(f"Tipo de `email`: {type(email)}")

            # Enviar el correo
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],  # Asegúrate de que esto sea una lista de un solo correo
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

def activation_failed(request):
    return render(request, 'registration/activation_failed.html')

def activate(request, uidb64, token):
    try:
        # Decodificar UID y asegurarse de que es válido
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = get_user_model().objects.get(pk=int(uid))  # Asegúrate de que sea un entero
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
        print("Error al decodificar el UID o encontrar el usuario.")
    
    if user is not None:
        comprobacion = default_token_generator.check_token(user, token)
        
        if comprobacion:
            user.is_active = True
            user.save()
            login(request, user, backend='users.backends.EmailBackend')
            return render(request, 'landing_page.html')
    
    return render(request, 'registration/activation_failed.html')



def logout_view(request):
    logout(request)
    return redirect('landing_page') 
   
#WISHLIST
@login_required    
def wishlist_add(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            animal_id = data.get("animal_id")
            interaction_type = data.get("interaction_type")
            animal = Animal.objects.get(id=animal_id)

            Wishlist.objects.create(
                user=request.user,animal=animal, interaction_type=interaction_type
            )

            return JsonResponse({'status': 'success', 'message': 'Interacción registrada.'})
        except Animal.DoesNotExist:
            return JsonResponse({'status':'error', 'message':'Animal no encontrado.'})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Método no permitido."})

    # animal = get_object_or_404(Animal, id=animal_id)
    # if request.method == 'POST':
    #     interaction_type = request.POST.get('interaction_type')
    #     Wishlist.objects.get_or_create(user=request.user, animal=animal, interaction_type=interaction_type)
    #     return redirect('wishlist_list')
    # return render(request, 'add_to_wishlist.html', {'animal': animal})

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
            return render(request, 'test/adoption_result.html', {'especie': especie})
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
            return render(request, 'test/adoption_result.html', {'especie': especie})
    else:
        form = TestGatoForm()
    return render(request, 'cat_test.html', {'form': form, 'especie': especie})

def resultado_test(request):
    if request.method == "POST":
        respuestas = {
            'tamaño': request.POST.get('tamaño'),
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
        request.session['respuestas'] = respuestas
        especie = request.POST.get('especie')  # Esta respuesta debería venir de alguna parte
        if especie == 'perro':
            form = TestPerroForm(respuestas)
        elif especie == 'gato':
            form = TestGatoForm(respuestas)
        else:
            return render(request, 'error.html', {'mensaje': 'Especie no válida.'})
        
        animales = Animal.objects.filter(species=especie)

        puntuaciones = []
        for animal in animales:
            # Comparar las respuestas del usuario con los atributos del animal
            puntuacion = 0
            if respuestas['tamaño'].lower() == animal.size.lower():
                puntuacion += 3
            if respuestas['energia'].lower() == animal.energy.lower():
                puntuacion += 3
            if respuestas['pelaje'].lower() == animal.fur.lower():
                puntuacion += 3
            if respuestas['caracter'].lower() == animal.personality.lower():
                puntuacion += 3

            # Si es un perro, evaluamos los campos adicionales específicos de perros
            if especie == 'perro':
                if respuestas['paseo'] == animal.energy:  # Ejercicio y energía se correlacionan para perros
                    puntuacion += 3

            # Si es un gato, evaluamos los campos adicionales específicos de gatos
            if especie == 'gato':
                # Para los gatos, podríamos agregar atributos como "actividad", si fuera relevante
                if respuestas.get('actividad', '') == animal.energy:  # Adaptamos energía para gatos
                    puntuacion += 3

            puntuaciones.append((animal, puntuacion))
        
        # Ordenar los animales por la puntuación más alta
        puntuaciones.sort(key=lambda x: x[1], reverse=True)

        if puntuaciones:
            animal_ideal = puntuaciones[0][0]  # Accedemos al primer elemento de la tupla (animal)
        else:
            animal_ideal = None

    # Pasar el resultado a la plantilla
    return render(request, 'test/adoption_result.html', {
        'animal_ideal': animal_ideal,
        'especie': especie,
    })
def admin_only(user):
    return user.is_authenticated and user.is_staff

# @user_passes_test(admin_only)
# def export_animals_csv(request):
#     animals = Animal.objects.all()

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="animals.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['ID', 'Name', 'Age', 'Species', 'Description', 'Image', 'Adoption_status'])

#     for animal in animals:
#         writer.writerow([animal.id, animal.name, animal.age, animal.species, animal.description, animal.image, animal.adoption_status])

#     return response

# @user_passes_test(admin_only)
# def export_interactions_csv(request):
#     interactions = Wishlist.objects.all()

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="interactions.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['ID', 'User', 'Animals', 'Interaction_type'])

#     for interaction in interactions:
#         writer.writerow([interaction.id, interaction.user, interaction.animals, interaction.interaction_type])
    
#     return response

@login_required
def user_dashboard(request):
    user = request.user

    recommendations = get_user_recommendations(user)

    return render(request, 'recommend/list.html', {'recommended_animals':recommendations})

# @login_required
# def get_recommendations(request):
#     recommended_animals = user_dashboard(request.user)

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