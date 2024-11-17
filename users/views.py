from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm,AdoptionApplicationCreationForm
from .models import CustomUser,AdoptionApplication
from django.views.generic import CreateView,ListView,View

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

# Create your views here.

# Vista para la landing page
def landing_page(request):
    return render(request, 'landing_page.html')

class AdoptionApplicationCreateView(CreateView):
    model = AdoptionApplication
    form_class = AdoptionApplicationCreationForm
    template_name = 'adoption_application/create.html'
    success_url = reverse_lazy('solicitud_adopcion_confirm')

class AdoptionApplicationConfirmationView(ListView):
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