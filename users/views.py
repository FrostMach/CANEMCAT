import json
import smtplib
import requests

from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View, generic
from django.contrib.auth import views as auth_views
from shelters.models import AdoptionApplication, Animal, StatusEnum
from users.sys_recommend.sys_recommend import get_user_recommendations
from .forms import CustomUserCreationForm, CustomUserChangeForm,AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser, Wishlist, Test, AdopterProfile, ShelterWorkerProfile, News
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import LoginForm
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete

from shelters.models import Animal, Shelter
from users.sys_recommend.csv_util import export_wishlist_to_csv, generate_animal_data
from users.sys_recommend.recommendations import recommend_from_csv
from .forms import CustomUserCreationForm, CustomUserChangeForm, LoginForm, TestPerroForm, TestGatoForm
from .models import CustomUser, ShelterWorkerProfile, Wishlist, Test, AdopterProfile

import tensorflow as tf
import os

@never_cache
def landing_page(request):
    # Obtener todas las noticias
    news = News.objects.all()  # Si quieres ordenarlas por fecha, puedes hacerlo con .order_by('-created_at')
    
    # Obtener los animales (si es necesario para el slider de animales)
    animals = Animal.objects.all()
    
    return render(request, 'landing_page.html', {
        'is_landing_page': True,
        'news': news,  # Pasar las noticias al template
        'animals': animals,  # Pasar los animales al template
    })

#CANEMSCAN
from django.http import JsonResponse
from django.conf import settings
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Función para extraer características dinámicamente con un modelo dado
def extract_features(image_path, model):
    """
    Extrae un vector de características de una imagen usando el modelo proporcionado.
    """
    feature_extractor = Model(inputs=model.input, outputs=model.layers[-2].output)  # Crear el extractor dinámicamente
    img = load_img(image_path, target_size=(224, 224))  # Redimensionar la imagen
    img_array = img_to_array(img) / 255.0  # Normalizar
    img_array = img_array.reshape((1, 224, 224, 3))  # Añadir dimensión batch
    features = feature_extractor.predict(img_array)  # Extraer características
    return features.flatten()  # Devolver como un vector 1D

# Función para obtener imágenes y características de la base de datos
def get_animal_images_and_features(animal_type, model):
    """
    Recupera las imágenes y características de perros o gatos según el tipo de animal.
    """
    animals = Animal.objects.filter(species=animal_type)  # Filtrar según el tipo
    images_and_features = []

    for animal in animals:
        image_path = animal.image.path
        if os.path.exists(image_path):
            features = extract_features(image_path, model)
            images_and_features.append((animal, features))

    return images_and_features

#COMPARADOR DE IMÁGENES
from scipy.spatial.distance import cosine

# Función para encontrar imágenes similares
def find_similar_images(uploaded_image_path, animal_features, model, top_n=4):
    """
    Encuentra las imágenes más similares a la imagen cargada.
    """
    uploaded_features = extract_features(uploaded_image_path, model)  # Pasar modelo cargado
    similarities = []

    for animal, features in animal_features:
        similarity = 1 - cosine(uploaded_features, features)  # Similitud basada en el coseno
        similarities.append((animal, similarity))

    # Ordenar por similitud descendente
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    return similarities[:top_n]  # Devolver las N más similares

def canem_scan(request):
    if request.method == 'POST':
        animal_type = request.POST.get('animal_type')  # Recoge el tipo seleccionado por el usuario
        request.session['animal_type'] = animal_type  # Guarda en la sesión
    return render(request, 'canemscan.html')

BREEDS = ['Affenpinscher', 'American Staffordshire Terrier', 'Basenji', 'Basset Hound', 'Beagle', 'Bedlington Terrier', 'Bichón maltés', 'Black and Tan Coonhound', 'Bluetick Coonhound', 'Bobtail', 'Border Collie', 'Border Terrier', 'Borzoi', 'Boston Terrier', 'Boxer', 'Boyer de Entlebuch', 'Boyero de Appenzell', 'Boyero de Berna', 'Boyero de Flandes', 'Braco alemán de pelo corto', 'Braco de Weimar', 'Bull Terrier', 'Bulldog francés', 'Bullmastiff','Cairn Terrier', 'Caniche enano', 'Cavalier King Charles Spaniel', 'Cazador de alces noruego', 'Chihuahua', 'Chin japonés', 'Chow Chow', 'Clumber Spaniel', 'Cobrador de pelo liso', 'Cocker inglés', 'Collie', 'Corgi galés de Cardigan', 'Corgi galés de Pembroke', 'Cuon alpinus', 'Dachshund', 'Dandie Dinmont Terrier', 'Dingo', 'Doberman', 'Dogo del Tíbet', 'Dálmata', 'Esquimal americano', 'Fox Terrier de pelo duro', 'Foxhound inglés', 'Galgo italiano', 'Golden Retriever', 'Gordon Setter', 'Gran boyer suizo', 'Gran danés', 'Husky siberiano', 'Keeshond', 'Kelpie australiano', 'Kerry Blue Terrier', 'Komondor', 'Kuvasz húngaro', 'Labrador Retriever', 'Lakeland Terrier', 'Lebrel afgano', 'Lebrel escocés', 'Leonberger', 'Lhasa Apso', 'Lobero irlandés', 'Malamute de Alaska', 'Otterhound', 'Papillón', 'Pastor alemán', 'Pastor belga Groenendael', 'Pastor belga Malinois', 'Pastor de Brie', 'Pastor de islas Shetland', 'Pekinés', 'Perro crestado rodesiano', 'Perro de agua irlandés', 'Perro de montaña de los Pirineos', 'Perro de San Huberto', 'Perro salvaje africano', 'Petit Brabançon', 'Pinscher miniatura', 'Podenco ibicenco', 'Pomeranian', 'Poodle estándar', 'Poodle Toy', 'Pug', 'Redbone Coonhound', 'Retriever de Chesapeake', 'Retriever de pelo rizado', 'Rottweiler', 'Saluki', 'Samoyedo', 'San Bernardo', 'Schipperke', 'Schnauzer estándar', 'Schnauzer gigante', 'Schnauzer miniatura', 'Sealyham Terrier', 'Setter inglés', 'Setter irlandés', 'Shiba Inu', 'Shih Tzu', 'Silky Terrier australiano', 'Soft Coated Wheaten Terrier', 'Spaniel Bretón', 'Springer spaniel galés', 'Springer Spaniel inglés', 'Staffordshire Bull Terrier', 'Sussex Spaniel', 'Terranova', 'Terrier de Airedale', 'Terrier de Australia', 'Terrier de Norfolk', 'Terrier de Norwich', 'Terrier escocés', 'Terrier irlandés', 'Terrier tibetano', 'Toy Terrier inglés', 'Treeing Walker Coonhound', 'Vizsla', 'West Highland White Terrier', 'Whippet', 'Xoloitzcuintle', 'Yorkshire Terrier']  # Actualiza según tu entrenamiento
BREEDS2 = breeds = ['Abisinio', 'Americano de pelo corto', 'Angora turco', 'Azul ruso', 'Bengalí', 'Birmano', 'Bobtail americano', 'Bombay', 'Británico de pelo corto', 'Curl americano', 'Esfinge', 'Exótico', 'Fold escocés', 'Gato de bosque de Noruega', 'Maine Coon', 'Manx', 'Mau egipcio', 'Persa', 'Ragdoll', 'Siamés']  # Lista de razas de gatos

def upload_image(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # Recuperar el tipo de animal desde la sesión
        animal_type = request.session.get('animal_type', None)

        # Verificar que animal_type está presente
        if not animal_type:
            return JsonResponse({'error': 'El tipo de animal no está definido en la sesión.'}, status=400)

        uploaded_file = request.FILES['image']

        # Seleccionar modelo y razas según el tipo de animal
        if animal_type == 'gato':
            model_path = os.path.join(settings.BASE_DIR, 'Users', 'IA', 'CanemSCANCAT.keras')
            breeds = BREEDS2
        elif animal_type == 'perro':
            model_path = os.path.join(settings.BASE_DIR, 'Users', 'IA', 'CanemSCAN2200.h5')
            breeds = BREEDS
        else:
            return JsonResponse({'error': 'Tipo de animal no válido.'}, status=400)

        model = load_model(model_path)
        
        # Guardar temporalmente la imagen
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded')
        os.makedirs(upload_dir, exist_ok=True)
        saved_path = os.path.join(upload_dir, uploaded_file.name)

        with open(saved_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        try:
            # Extraer características usando el modelo seleccionado
            features = extract_features(saved_path, model)
            # Preprocesar la imagen
            img = load_img(saved_path, target_size=(224, 224))  # Tamaño esperado por el modelo
            img_array = img_to_array(img) / 255.0  # Normalización
            img_array = img_array.reshape((1, 224, 224, 3))  # Asegurar las dimensiones correctas

            # Realizar predicción
            predictions = model.predict(img_array)  # Devuelve probabilidades
            predicted_index = predictions.argmax()  # Índice de la probabilidad más alta
            predicted_breed = breeds[predicted_index]  # Obtener la raza correspondiente
            
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


# Vista para guardar el tipo de animal en la sesión
@csrf_exempt
def guardar_animal(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            animal_type = data.get('animal_type')

            if animal_type in ['perro', 'gato']:
                request.session['animal_type'] = animal_type
                return JsonResponse({'success': f'Animal tipo {animal_type} guardado en la sesión.'})
            else:
                return JsonResponse({'error': 'Valor inválido para animal_type.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido. Solo POST.'}, status=405)

from django.urls import reverse

def compare_images(request):
    # Recuperar el nombre del archivo subido desde la solicitud GET
    image_id = request.GET.get('uploaded_image_id', None)
    if not image_id:
        return JsonResponse({"error": "No se proporcionó el ID de la imagen."}, status=400)

    # Determinar el tipo de animal (priorizar la sesión si está disponible)
    animal_type = request.GET.get('animal_type', None)
    if not animal_type:
        animal_type = request.session.get('animal_type', 'gato')  # Por defecto 'gato' si no está en la sesión

    # Ruta a la imagen subida por el usuario
    uploaded_image_path = os.path.join(settings.MEDIA_ROOT, 'uploaded', image_id)
    if not os.path.exists(uploaded_image_path):
        return JsonResponse({'error': 'La imagen subida no se encuentra.'}, status=404)

    try:
        # Seleccionar modelo según el tipo de animal
        if animal_type == 'gato':
            model_path = os.path.join(settings.BASE_DIR, 'Users', 'IA', 'CanemSCANCAT.keras')
        else:
            model_path = os.path.join(settings.BASE_DIR, 'Users', 'IA', 'CanemSCAN2200.h5')
        
        model = load_model(model_path)  # Cargar el modelo

        # Obtener características de las imágenes en la base de datos
        animal_features = get_animal_images_and_features(animal_type, model)  # Pasar el modelo aquí
        if not animal_features:
            return JsonResponse({"error": f"No hay imágenes de {animal_type}s en la base de datos para comparar."}, status=404)

        # Encontrar las imágenes más similares
        similar_images = find_similar_images(uploaded_image_path, animal_features, model)  # Pasar el modelo aquí también

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

    def form_valid(self, form):
        user = form.save()

        if form.cleaned_data.get('user_type') == 'worker':
            return redirect('assign_worker', kwargs={'worker_id': user.id})
        
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('login')

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
            if user.user_type == 'adopter':
                AdopterProfile.objects.create(user=user)
            elif user.user_type == 'worker':
                ShelterWorkerProfile.objects.create(user=user)
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
            return render(request, 'test/error.html', {'mensaje': 'Especie no válida.'})
        
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
            animales_adecuados = [animal[0] for animal in puntuaciones[:4]]
        else:
            animales_adecuados = []

    # Pasar el resultado a la plantilla
    return render(request, 'test/adoption_result.html', {
        'animales_adecuados': animales_adecuados,
        'especie': especie,
    })


@login_required
def adoption_application_view(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id)

    # Verificar si el usuario es un adoptante
    if request.user.user_type != 'adopter':
        # Si el usuario no es un adoptante, redirigir o mostrar un mensaje de error
        return redirect('error_user_type')  # Puedes personalizar este redireccionamiento

    # Obtener el perfil de AdopterProfile asociado al usuario
    user_profile = AdopterProfile.objects.get(user=request.user)

    # Si el método es POST, creamos la solicitud de adopción
    if request.method == 'POST':
        # Crear la solicitud de adopción
        adoption_application = AdoptionApplication(
            user=user_profile,  # Usar el perfil de adoptante
            animal=animal,
            shelter=animal.shelter,  # La protectora del animal
            status='P',  # Por defecto, la solicitud está pendiente
        )
        adoption_application.save()

        # Redirigir al usuario a la lista de solicitudes o una página de confirmación
        return redirect('adoption_application_list')  # Personaliza esta URL según tu caso

    return render(request, 'adoption_application/adoption_application_request.html', {'animal': animal})

def error_user_type(request):
    return render(request, 'shelter/error_tipo_usuario.html')

@login_required
def adoption_application_list(request):
    # Obtener el perfil de adoptante del usuario
    user_profile = AdopterProfile.objects.get(user=request.user)
    
    # Obtener todas las solicitudes de adopción del usuario
    adoption_applications = AdoptionApplication.objects.filter(user=user_profile)

    return render(request, 'adoption_application/adoption_application_list.html', {'adoption_applications': adoption_applications})

@login_required
def adoption_application_list_shelterworker(request):
    # Verificar que el usuario es un "Shelter Worker"
    if request.user.user_type != 'worker':
        return redirect('error_user_type')  # Redirigir a un error si no es un "Shelter Worker"
    
    # Obtener el perfil del trabajador de la protectora
    shelter_worker_profile = get_object_or_404(ShelterWorkerProfile, user=request.user)

    # Verificar si el perfil tiene un "shelter" válido
    if not shelter_worker_profile.shelter_name:
        return render(request,'adoption_application/error_shelter_missing.html')  # Redirigir o mostrar error si no tiene un shelter

    # Obtener todas las solicitudes de adopción de los animales de la protectora del trabajador
    adoption_applications = AdoptionApplication.objects.filter(shelter=shelter_worker_profile.shelter_name)

    # Pasar las solicitudes a la plantilla
    return render(request, 'adoption_application/adoption_application_list_shelterworker.html', {
        'adoption_applications': adoption_applications
    })

@login_required
def update_adoption_application(request, application_id):
    # Verificar que el usuario es un "Shelter Worker"
    if request.user.user_type != 'worker':
        return redirect('error_user_type')  # Redirigir a un error si no es un "Shelter Worker"

    # Obtener la solicitud de adopción
    application = get_object_or_404(AdoptionApplication, pk=application_id)

    # Verificar que la solicitud pertenezca a la misma protectora del trabajador
    shelter_worker_profile = ShelterWorkerProfile.objects.get(user=request.user)
    if application.shelter != shelter_worker_profile.shelter_name:
        return redirect('error_user_type')  # Si el trabajador no pertenece a la protectora, redirigir

    if request.method == 'POST':
        # Verificar si se ha aprobado o denegado la solicitud
        action = request.POST.get('action')

        if action == 'approve':
            application.status = StatusEnum.APPROVED.value[0]
        elif action == 'deny':
            application.status = StatusEnum.DENIED.value[0]
        
        application.save()  # Guardar los cambios

        # Redirigir después de actualizar
        return redirect('adoption_application_list_shelterworker')

    return render(request, 'adoption_application/adoption_application_update.html', {'application': application})

class RecommendationView(View):
       def get(self, request):
        try:
            # Generar o cargar los datos solo si es necesario
            generate_animal_data()

            user_id = request.user.id
            
            # Obtener las recomendaciones (asegúrate de que esta función retorne datos válidos)
            recommendations = recommend_from_csv(user_id)
            
            if recommendations.empty:  # Si no hay recomendaciones
                return render(request, 'recommend/list.html', {
                    'message': "No se encontraron recomendaciones basadas en tus preferencias."
                })
            
            # Convierte las recomendaciones a un formato de lista de diccionarios
            data = recommendations.to_dict('records')

            # Asegúrate de que las imágenes tengan el prefijo adecuado
            for animal in data:
                if 'image' in animal and animal['image']:
                    if not animal['image'].startswith('/media/'):
                        animal['image'] = f"/{animal['image']}"

            return render(request, 'recommend/list.html', {
                'recommended_animals': data
            })

        except FileNotFoundError as e:
            # Manejar errores específicos, por ejemplo, si no se encuentra el archivo CSV
            return render(request, 'recommend/list.html', {
                'error': f"Error al cargar los datos de animales: {str(e)}"
            })
        except Exception as e:
            # Manejo genérico de otros errores
            return render(request, 'recommend/list.html', {
                'error': f"Ha ocurrido un error inesperado: {str(e)}"
            })

@receiver(post_save, sender=Wishlist)
@receiver(post_delete, sender=Wishlist)
def update_wishlist_csv(sender, instance, **kwargs):
    export_wishlist_to_csv()

def add_shelter_worker(request, shelter_id):
    # Obtener la protectora
    shelter = get_object_or_404(Shelter, id=shelter_id)

    # Verificar que el usuario pertenece al shelter
    if not ShelterWorkerProfile.objects.filter(user=request.user, shelter=shelter).exists() and not request.user.is_superuser:
        messages.error(request, "No tienes permiso para añadir trabajadores a esta protectora.")
        return redirect('view_shelter', pk=shelter_id)

    # Obtener usuarios disponibles (usuarios sin shelter)
    available_users = CustomUser.objects.filter(user_type='worker' ,worker_profile__isnull=True)

    if request.method == "POST":
        user_id = request.POST.get("user_id")

        # Validar que se seleccionó un usuario
        if not user_id:
            messages.error(request, "Debes seleccionar un usuario.")
            return redirect('add-shelter-worker', shelter_id=shelter_id)

        # Verificar que el usuario existe y está disponible
        user_to_add = get_object_or_404(available_users, id=user_id)

        # Crear el perfil de trabajador
        ShelterWorkerProfile.objects.create(user=user_to_add, shelter=shelter)
        messages.success(request, f"El usuario {user_to_add.full_name} ha sido añadido a la protectora {shelter.name}.")
        return redirect('shelter_workers', shelter_id=shelter_id)

    return render(request, "worker/assign_worker.html", {
        "shelter": shelter,
        "available_users": available_users
    })

def shelter_workers(request, shelter_id):
    shelter = get_object_or_404(Shelter, id=shelter_id)
    workers = ShelterWorkerProfile.objects.filter(shelter=shelter)

    return render(request, 'worker/shelter_workers_list.html', {
        'shelter': shelter,
        'workers': workers
    })

def remove_worker(request, worker_id, shelter_id):
    worker = get_object_or_404(ShelterWorkerProfile, id=worker_id, shelter_id=shelter_id)
    worker.delete()
    messages.success(request, "El trabajador ha sido eliminado.")

    return redirect('shelter_workers', shelter_id=shelter_id)