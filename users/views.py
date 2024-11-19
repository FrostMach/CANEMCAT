from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Wishlist

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
    
    
#WISHLIST    

class AddToWishlistView(generic.ListView):
    
    model = Wishlist
    template_name = 'wish/list.html'
    context_object_name = 'add'

class RemoveFromWishlistView(generic.ListView):
    
    model = Wishlist
    template_name = 'wish/list.html'
    context_object_name = 'remove'


