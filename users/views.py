from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm, AnimalForm,AdoptionApplicationCreationForm
from .models import CustomUser, Animal, Wishlist,AdoptionApplication

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
    
class AnimalDetailView(generic.DetailView):
    model = Animal
    template_name = 'animals/details.html' 
    context_object_name = 'animal'  
    

class AddToWishlistView(generic.ListView):
    
    model = Wishlist
    template_name = 'wish/list.html'
    context_object_name = 'add'

class RemoveFromWishlistView(generic.ListView):
    
    model = Wishlist
    template_name = 'wish/list.html'
    context_object_name = 'remove'

class AdoptionApplicationCreateView(generic.CreateView):
    model = AdoptionApplication
    form_class = AdoptionApplicationCreationForm
    template_name = 'adoption_application/create.html'
    success_url = reverse_lazy('solicitud_adopcion_confirm')

class AdoptionApplicationConfirmationView(generic.ListView):
    model = AdoptionApplication
    fields = ['user','animal','center']
    template_name = 'adoption_application/confirm.html'
    success_url = reverse_lazy('landing_page')

def create_adoption_application(request):
    if request.method == 'POST':
        form = AdoptionApplicationCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')
        else:
            return render(request, 'form_template.html', {'form': form})
    else:
        form = AdoptionApplicationCreationForm()
        return render(request, 'form_template.html', {'form': form})
def confirm_view(request):
    return render(request, 'adoption_application/confirm.html')
