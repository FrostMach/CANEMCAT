from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm, AnimalForm
from .models import CustomUser, Animal

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
    
#ANIMALES

class AnimalCreateView(generic.CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/create.html'
    success_url = reverse_lazy('animals-list')

class AnimalUpdateView(generic.UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/update.html'
    success_url = reverse_lazy('animals-list')

class AnimalDeleteView(generic.DeleteView):
    model = Animal
    template_name = 'animals/delete.html'
    success_url = reverse_lazy('animals-list')

class AnimalListView(generic.ListView):
    model = Animal
    template_name = 'animals/list.html'
    context_object_name = 'animals'

    def get_queryset(self):
        return Animal.objects.all()


