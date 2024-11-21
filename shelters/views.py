from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import RegisterShelterForm, UpdateShelterForm

from .models import Shelter

# Create your views here.

# Vista para la landing page
def landing_page(request):
    return render(request, 'landing_page.html')

class RegisterShelterView(generic.CreateView):
    model = Shelter
    form_class = RegisterShelterForm
    template_name = 'shelter/register.html'
    success_url = reverse_lazy('exit_register')

class ShelterView(generic.DetailView):
    model = Shelter
    template_name = 'shelter/profile.html'
class UpdateShelterView(generic.UpdateView):
    model = Shelter
    form_class = UpdateShelterForm
    template_name = 'shelter/edit.html'
    
    def get_success_url(self):
        return reverse('view_shelter', kwargs={'pk':self.object.pk})

class DeleteShelterView(generic.DeleteView):
    model = Shelter
    template_name = 'shelter/delete_confirm.html'
    success_url = reverse_lazy('register_shelter')