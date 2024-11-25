from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Wishlist
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm
from django.contrib.auth.forms import UserCreationForm

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
