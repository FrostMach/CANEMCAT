from django.shortcuts import render, redirect, get_object_or_404
from shelters.models import Animal, AdoptionApplication, Shelter
from django.urls import reverse_lazy, reverse
from shelters.forms import AdoptionApplicationCreationForm, AnimalForm, CompleteShelterForm, RegisterShelterForm, UpdateShelterForm
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from shelters.forms import AdoptionApplicationCreationForm, AnimalForm, RegisterShelterForm, UpdateShelterForm, AnimalFilterForm
from django.views import View, generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from math import atan2, cos, radians, sin, sqrt
from django.http import JsonResponse
from .models import Animal

from users.models import Wishlist

# Create your views here.

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
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        form = AnimalFilterForm(self.request.GET)

        if form.is_valid():
            # Filtros según los valores del formulario
            species = form.cleaned_data.get("species")
            sex = form.cleaned_data.get("sex")
            size = form.cleaned_data.get("size")
            shelter = form.cleaned_data.get("shelter")

            if species:
                queryset = queryset.filter(species=species)
            if sex:
                queryset = queryset.filter(sex=sex)
            if size:
                queryset = queryset.filter(size=size)
            if shelter:
                queryset = queryset.filter(shelter=shelter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = AnimalFilterForm(self.request.GET)  # Pasa el formulario al contexto
        return context
    
class AnimalShelterListView(generic.ListView):
    model = Animal
    template_name = 'shelter/animal_list.html'
    context_object_name = 'animal_list'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        form = AnimalFilterForm(self.request.GET)

        if form.is_valid():
            # Filtros según los valores del formulario
            species = form.cleaned_data.get("species")
            sex = form.cleaned_data.get("sex")
            size = form.cleaned_data.get("size")
            shelter = form.cleaned_data.get("shelter")

            if species:
                queryset = queryset.filter(species=species)
            if sex:
                queryset = queryset.filter(sex=sex)
            if size:
                queryset = queryset.filter(size=size)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = AnimalFilterForm(self.request.GET)  # Pasa el formulario al contexto
        return context
    
class AnimalDetailView(generic.DetailView):
    model = Animal
    template_name = 'animals/details.html' 
    context_object_name = 'animal'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = self.object

        if self.request.user.is_authenticated:
            if not Wishlist.objects.filter(user=self.request.user, animal=animal,
                interaction_type='view').exists():
                Wishlist.objects.create(user=self.request.user, animal=animal, interaction_type='view')

        context['is_in_wishlist'] = Wishlist.objects.filter(
            user = self.request.user,
            animal = animal,
            interaction_type='favorite').exists()

        return context
    
#SOLICITUD DE ADOPCIÓN    
    
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

#SHELTERS
@staff_member_required
def shelter_approval(request, shelter_id):
    shelter = get_object_or_404(Shelter, id=shelter_id)

    if not request.user.is_staff:
        raise PermissionDenied('No tienes permiso para aprobar la acreditación.')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            shelter.status = True
        elif action == 'reject':
            shelter.status = False
        
        shelter.save()
        return redirect('register_complete', shelter_id=shelter_id)
    
    return render(request, 'shelter/approve.html', {'shelter': shelter})

def admin_only(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(admin_only)
def register_shelter(request):
    if request.method == 'POST':
        form = RegisterShelterForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('shelter_list')
    else:
        form = RegisterShelterForm()

    return render(request, 'shelter/register.html', {'form': form})

@staff_member_required
def complete_shelter_registration(request, shelter_id):
    shelter = get_object_or_404(Shelter, id=shelter_id)

    if request.method == 'POST':
        form = CompleteShelterForm(request.POST, instance=shelter)
        
        if form.is_valid():
            form.save()
            return redirect('shelter_list')
    
    else:
        form = CompleteShelterForm(instance=shelter)

    return render(request, 'shelter/complete_registration.html', {'form': form, 'shelter': shelter})

class ShelterList(generic.ListView):
    model = Shelter
    template_name = 'shelter/list.html'
    context_object_name = 'shelters'

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

def check_acreditation(request, shelter_id):
    shelter = get_object_or_404(Shelter, id=shelter_id)

    return render(request, 'shelter/profile.html', {'shelter': shelter})

def nearby_shelters(request):
    lat = request.GET.get('latitude')
    lon = request.GET.get('longitude')

    shelters = Shelter.objects.all()
    data = [
        {'name': shelter.name, 
         'address': shelter.address, 
         'latitude':shelter.latitude, 
         'longitude':shelter.longitude} 
         for shelter in shelters
    ]

    return JsonResponse(data, safe=False)

def map_view(request):
    return render(request, 'shelter/nearby_shelter.html')

def shelters_by_postal_code(request):
    postal_code = request.GET.get('postal_code', '').strip()

    if not postal_code:
        return JsonResponse({'error':'Postal code is required'}, status=400)
    
    shelters = Shelter.objects.filter(postal_code=postal_code).values(
        'name', 'address', 'latitude', 'longitude'
    )

    return JsonResponse(list(shelters),safe=False)
# def calculate_distance(lat1, lon1, lat2, lon2):
#     R = 6371.0
#     dlat = radians(lat2 - lat1)
#     dlon = radians(lon2 - lon1)
#     a = sin(dlat/2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
#     c = 2 * atan2(sqrt(a), sqrt(1-a))
    
#     return R * c

def landing_page2(request):
    return render(request, 'shelter/landing_page2.html')