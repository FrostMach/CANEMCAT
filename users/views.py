from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic

from shelters.models import Animal
# from sys_recommend.sys_recommend import recommend_pets
from .forms import CustomUserCreationForm, CustomUserChangeForm,AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from .models import AdopterProfile, CustomUser, Wishlist
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import smtplib
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import csv

def landing_page(request):
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
                return redirect('dashboard')  # Redirige a la página principal o dashboard
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