from django.shortcuts import render, redirect, get_object_or_404
from shelters.models import Animal, AdoptionApplication, Shelter
from django.urls import reverse_lazy, reverse
from shelters.forms import AdoptionApplicationCreationForm, AnimalForm, RegisterShelterForm, UpdateShelterForm
from django.views import generic
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from shelters.forms import AdoptionApplicationCreationForm, AnimalForm, RegisterShelterForm, UpdateShelterForm, AnimalFilterForm
from django.views import View, generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from math import atan2, cos, radians, sin, sqrt
from django.http import JsonResponse
from .models import Animal, Event
from django.core.paginator import Paginator
from users.models import Wishlist
import json
from django.utils.dateparse import parse_date, parse_time, parse_datetime
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
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

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         animal = self.object

#         is_in_wishlist = False

#         if user.is_authenticated:
#             is_in_wishlist = Wishlist.objects.filter(user=user, animal=animal).exists()
#             Wishlist.objects.create(user=user, animal=animal, interaction_type='view')
        
#         context['is_in_wishlist'] = is_in_wishlist

#         return context
    
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
        return redirect('shelter_list')
    
    return render(request, 'shelter/list_pending.html', {'shelter': shelter})

@login_required
def register_shelter(request):
    if request.method == 'POST':
        form = RegisterShelterForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('shelter_list')
    else:
        form = RegisterShelterForm()

    return render(request, 'shelter/register.html', {'form': form})

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