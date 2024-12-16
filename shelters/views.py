from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required
from shelters.forms import AdoptionApplicationCreationForm, AnimalForm, RegisterShelterForm, UpdateShelterForm, AnimalFilterForm
from django.views import View, generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from math import atan2, cos, radians, sin, sqrt
from django.http import JsonResponse
from .models import Animal
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseForbidden
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from shelters.models import Animal, AdoptionApplication, Shelter
from shelters.forms import AdoptionApplicationCreationForm, AnimalForm, CompleteShelterForm, RegisterShelterForm, UpdateShelterForm, AnimalFilterForm
from .models import Animal
from users.models import Wishlist

from users.models import Wishlist
import json
from django.utils.dateparse import parse_date, parse_time, parse_datetime
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from users.models import Wishlist, AdopterProfile

# Create your views here.

#Calendar
# myapp/views.py

# Vista principal, que muestra los eventos en la plantilla (si lo necesitas)
def index(request):
    all_events = Event.objects.all()
    context = {
        "events": all_events,
    }
    return render(request, 'shelter/navegador/calendar.html', context)

# Vista para obtener todos los eventos
def all_events(request):
    all_events = Event.objects.all()
    out = []
    for event in all_events:                                                                                             
        # Verificar si start_time y end_time no son None antes de formatearlos
        start_time = event.start_time.strftime("%Y-%m-%d %H:%M:%S") if event.start_time else None
        end_time = event.end_time.strftime("%Y-%m-%d %H:%M:%S") if event.end_time else None
        
        out.append({                                                                                                     
            'title': event.description,  # Cambié 'name' a 'description' según tu modelo
            'id': event.id,                                                                                              
            'start': start_time,  # Asignamos el valor formateado o None
            'end': end_time,  # Asignamos el valor formateado o None
        })  
    return JsonResponse(out, safe=False)

# Vista para agregar un nuevo evento
def add_event(request):
    if request.method == "POST":
        title = request.POST.get('title')
        start = request.POST.get('start')  # Fecha de inicio recibida como cadena
        end = request.POST.get('end')  # Fecha de fin recibida como cadena

        # Verificar si las fechas están en formato correcto
        try:
            start_time = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")  # Convierte la fecha de inicio
            end_time = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")  # Convierte la fecha de fin
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Formato de fecha inválido'}, status=400)

        # Crear el evento
        event = Event.objects.create(
            description=title,
            start_time=start_time,
            end_time=end_time,
        )

        return JsonResponse({'status': 'success', 'message': 'Evento creado correctamente'}, status=201)
    return JsonResponse({'status': 'error', 'message': 'Petición inválida'}, status=400)

# Vista para actualizar un evento existente
def update(request):
    if request.method == 'POST':
        try:
            # Obtener los datos enviados desde la solicitud
            event_id = request.POST.get('id')
            start_time = request.POST.get('start')  # Formato esperado: "YYYY-MM-DD HH:mm:ss"
            end_time = request.POST.get('end')  # Formato esperado: "YYYY-MM-DD HH:mm:ss"
            
            # Validar los datos recibidos
            if not (event_id and start_time and end_time):
                return JsonResponse({'success': False, 'message': 'Datos incompletos'})

            # Convertir las fechas de string a objetos datetime
            start_time_obj = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

            # Buscar el evento en la base de datos
            event = Event.objects.get(id=event_id)

            # Actualizar las fechas y guardar el evento
            event.start_time = start_time_obj
            event.end_time = end_time_obj
            event.save()

            return JsonResponse({'success': True, 'message': 'Evento actualizado correctamente'})
        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El evento no existe'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

# Vista para eliminar un evento
def remove(request):
    if request.method == "POST":
        event_id = request.POST.get('id')  # Obtener el ID del evento enviado desde el frontend
        try:
            event = Event.objects.get(id=event_id)  # Intentar obtener el evento por ID
            event.delete()  # Eliminar el evento
            return JsonResponse({'status': 'success', 'message': 'Event removed successfully'})
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Event does not exist'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

#ANIMALES

class AnimalCreateView(generic.CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/create.html'
    success_url = reverse_lazy('animal_list')

class AnimalUpdateView(generic.UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/update.html'
    success_url = reverse_lazy('animals-list')

class AnimalDeleteView(generic.DeleteView):
    model = Animal
    template_name = 'animals/delete.html'
    success_url = reverse_lazy('animal_list')

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
            adoption_status = form.cleaned_data.get("adoption_status")
            shelter = form.cleaned_data.get("shelter")

            if adoption_status:
                adoption_status = adoption_status.capitalize()  # Asegura que el valor tiene la primera letra mayúscula

            if species:
                queryset = queryset.filter(species=species)
            if sex:
                queryset = queryset.filter(sex=sex)
            if size:
                queryset = queryset.filter(size=size)
            if adoption_status:
                queryset = queryset.filter(adoption_status=adoption_status)
            if shelter:
                queryset = queryset.filter(shelter=shelter)

        queryset = queryset.order_by('id')  # O usa otro campo para ordenar según tus necesidades

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
            adoption_status = form.cleaned_data.get("adoption_status")
            shelter = form.cleaned_data.get("shelter")
            
            if adoption_status:
                adoption_status = adoption_status.capitalize()  # Asegura que el valor tiene la primera letra mayúscula
            
            if species:
                queryset = queryset.filter(species=species)
            if sex:
                queryset = queryset.filter(sex=sex)
            if size:
                queryset = queryset.filter(size=size)
            if adoption_status:
                queryset = queryset.filter(adoption_status=adoption_status)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = AnimalFilterForm(self.request.GET)  # Pasa el formulario al contexto
        return context

def animals_list(request, shelter_id):
    # Obtener la protectora actual
    shelter = get_object_or_404(Shelter, id=shelter_id)
    
    # Obtener animales de esa protectora
    animals = Animal.objects.filter(shelter=shelter)
    
    # Aplicar filtros si se usan
    filter_form = AnimalFilterForm(
        request.GET,
        shelter_queryset=Shelter.objects.filter(id=shelter_id)  # Solo la protectora actual
    )
    
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('species'):
            animals = animals.filter(species=filter_form.cleaned_data['species'])
        if filter_form.cleaned_data.get('sex'):
            animals = animals.filter(sex=filter_form.cleaned_data['sex'])
        if filter_form.cleaned_data.get('size'):
            animals = animals.filter(size=filter_form.cleaned_data['size'])
        if filter_form.cleaned_data.get('adoption_status'):
            animals = animals.filter(adoption_status=filter_form.cleaned_data['adoption_status'])

    # Paginación
    paginated_animals = paginate(request, animals, per_page=9)

    return render(request, 'animals/list_animal_shelter.html', {
        'object_list': paginated_animals,  # Animales filtrados y paginados
        'filter_form': filter_form,        # Formulario de filtros
        'shelter': shelter,                # Protectora actual
        'is_paginated': paginated_animals.has_other_pages(),
        'page_obj': paginated_animals,
    })


def paginate(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

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
    


class AdoptionApplicationConfirmationView(generic.ListView):
    model = AdoptionApplication
    fields = ['user','animal','center']
    template_name = 'adoption_application/confirm.html'
    success_url = reverse_lazy('landing_page')

class AdoptionApplicationStatusView(generic.UpdateView):
    model = AdoptionApplication
    fields = ['status']
    template_name = 'adoption_application/status_update.html'
    success_url = reverse_lazy('solicitud_adopcion_confirm')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application'] = self.object
        return context

class UserAdoptionApplicationsView(generic.ListView):
    model = AdoptionApplication
    template_name = 'adoption_application/user_applications.html'

    def get_queryset(self):
        # Asegúrate de filtrar las solicitudes según el usuario actual
        return AdoptionApplication.objects.filter(user=self.request.user)


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

class ShelterRegistrationView(LoginRequiredMixin, CreateView):
    model = Shelter
    form_class = RegisterShelterForm
    template_name = 'shelter/register.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type not in ['worker', 'admin']:
            return HttpResponseForbidden('No tienes permisos para registrar una protectora')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('shelter_list')

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

    def get_context_data(self, **kwargs):
        # Este método agrega información adicional al contexto de la vista.
        context = super().get_context_data(**kwargs)
        # Puedes agregar información adicional aquí si es necesario.
        return context

class UpdateShelterView(generic.UpdateView):
    model = Shelter
    form_class = UpdateShelterForm
    template_name = 'shelter/edit.html'
    
    def get_success_url(self):
        return reverse('view_shelter', kwargs={'pk':self.object.pk})
    
    def get_form(self, form_class=None):
        # Sobrescribimos el método `get_form` para agregar las clases 'form-control' a todos los campos
        form = super().get_form(form_class)
        
        # Añadir la clase 'form-control' a cada campo del formulario
        for field in form:
            field.field.widget.attrs.update({'class': 'form-control'})
        
        return form

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

def landing_page2(request):
    if hasattr(request.user, 'worker_profile'):
        shelter = request.user.worker_profile.shelter
    else:
        shelter = None

    context = {
        'shelter': shelter,
    }
    
    return render(request, 'shelter/landing_page2.html', context)