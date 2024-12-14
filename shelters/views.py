from django.shortcuts import render, redirect, get_object_or_404
from shelters.models import Animal, AdoptionApplication, Shelter
from django.urls import reverse_lazy, reverse
from shelters.forms import AdoptionApplicationCreationForm, AnimalForm, RegisterShelterForm, UpdateShelterForm
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
from .models import Animal, Event
from django.core.paginator import Paginator
from users.models import Wishlist

# Create your views here.

#Calendar
def calendar_view(request):
    # Renderiza el calendario
    return render(request, 'shelter/navegador/calendar.html')

import json
from django.utils.dateparse import parse_date, parse_time
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Esto es si quieres permitir que se haga un POST sin CSRF token, puede ser necesario si se está usando en un formulario externo
def user_events(request):
    if not request.user.is_authenticated:
        # Si el usuario no está autenticado, redirige o muestra un mensaje de error
        return render(request, 'error.html', {'message': 'Por favor, inicie sesión para ver los eventos.'})

    # Obtener todos los eventos del usuario autenticado
    events = Event.objects.filter(user=request.user).order_by('date', 'start_time')

    # Paginación: Mostrar 5 eventos por página
    paginator = Paginator(events, 5)
    page = request.GET.get('page')
    events_page = paginator.get_page(page)

    # Pasar los eventos paginados a la plantilla
    # Pasar los eventos paginados a la plantilla
    return render(request, 'shelter/navegador/calendar.html', {
        'events': events_page,
        'is_paginated': events_page.has_other_pages(),  # Ver si hay más de una página
        'page_obj': events_page,  # El objeto de la página actual
})

@csrf_exempt
def edit_event(request, event_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validación de campos requeridos
            required_fields = ['description', 'date', 'start_time', 'end_time', 'color']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({'error': f'El campo {field} es obligatorio'}, status=400)

            # Obtener el evento por su ID
            try:
                event = Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                return JsonResponse({'error': 'Evento no encontrado'}, status=404)

            # Verificar permisos del usuario
            if event.user != request.user:
                return JsonResponse({'error': 'No tienes permisos para editar este evento'}, status=403)

            # Actualizar los campos del evento
            event.description = data['description']
            event.date = parse_date(data['date'])
            event.start_time = parse_time(data['start_time'])
            event.end_time = parse_time(data['end_time'])
            event.color = data['color']
            event.save()

            # Respuesta JSON con los datos actualizados
            return JsonResponse({
                'success': True,
                'event': {
                    'id': event.id,
                    'date': event.date.strftime('%Y-%m-%d'),
                    'description': event.description,
                    'start_time': event.start_time.strftime('%H:%M'),
                    'end_time': event.end_time.strftime('%H:%M'),
                    'color': event.color
                }
            })
        except ValueError:
            return JsonResponse({'error': 'Datos inválidos'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def delete_event(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(id=event_id)
        event.delete()
        return JsonResponse({'success': True})
    
def load_events(request, year, month):
    # Obtener los eventos del mes solicitado
    events = Event.objects.filter(date__year=year, date__month=month)
    
    event_data = []
    for event in events:
        event_data.append({
            'date': event.date.strftime('%Y-%m-%d'),
            'description': event.description,
            'start_time': event.start_time.strftime('%H:%M') if event.start_time else '',
            'end_time': event.end_time.strftime('%H:%M') if event.end_time else '',
            'color': event.color
        })
    
    return JsonResponse({'events': event_data})

from datetime import datetime

def save_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Convierte las fechas y horas a objetos datetime
        date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        
        description = data['description']
        color = data['color']
        user = request.user  # Suponiendo que el usuario está autenticado
        
        event = Event.objects.create(
            user=user,
            date=date,
            description=description,
            start_time=start_time,
            end_time=end_time,
            color=color
        )
        
        return JsonResponse({
            'success': True,
            'event': {
                'date': event.date.strftime('%Y-%m-%d'),
                'description': event.description,
                'start_time': event.start_time.strftime('%H:%M'),
                'end_time': event.end_time.strftime('%H:%M'),
                'color': event.color
            }
        })
    return JsonResponse({'success': False}, status=400)

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