from django.shortcuts import render, redirect, get_object_or_404
from shelters.models import Animal, AdoptionApplication, Shelter
from django.urls import reverse_lazy, reverse
from shelters.forms import AdoptionApplicationCreationForm, AnimalForm, RegisterShelterForm, UpdateShelterForm
from django.views import View, generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from math import atan2, cos, radians, sin, sqrt
from django.http import JsonResponse

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
    paginate_by = 5

    def get_queryset(self):
        return Animal.objects.all()
    
class AnimalDetailView(generic.DetailView):
    model = Animal
    template_name = 'animals/details.html' 
    context_object_name = 'animal'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        animal = self.object

        is_in_wishlist = False

        if user.is_authenticated:
            is_in_wishlist = Wishlist.objects.filter(user=user, animal=animal).exists()
        
        context['is_in_wishlist'] = is_in_wishlist

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
def is_admin(user):
    return user.is_staff

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class CheckDocumentView(generic.View):
    def get(self, request, pk):
        shelter = get_object_or_404(Shelter, pk = pk)  
        return render(request, 'shelter/pending.html', {'shelter':shelter}) 
     
    def post(self, request, pk):
        shelter = get_object_or_404(Shelter, pk=pk)
        action = request.POST.get('action')

        if action == 'aprobar':
            shelter.accreditation_status = True
        shelter.status = True
        shelter.save()

        return redirect('shelter_list')
        # shelter.accreditation_status = True
        # shelter.save()
        # messages.success(request, f'El centro "{shelter.name}" ha sido acreditado')
        # return redirect('check_pending')

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class ShelterListPendingView(generic.View):
    def get(self, request):
        shelters_pending = Shelter.objects.filter(status=False)
        return render(request, 'shelter/list_pending.html', {'shelters', shelters_pending})
    
class RegisterShelterView(generic.CreateView):
    def get(self, request):
        form = RegisterShelterForm()
        return render(request, 'shelter/register.html', {'form': form})
    
    def post(self, request):
        form = RegisterShelterForm(request.POST, request.FILES)
        
        if form.is_valid():
            shelter = form.save(commit=False)
            if shelter.accreditation_status:
                shelter.save()
                return redirect('exit_register')
            else:
                form.add_error(None, 'Solo centros acreditados pueden registrarse')
        
        return render(request, 'shelter/register.html', {'form': form})

    # model = Shelter
    # form_class = RegisterShelterForm
    # template_name = 'shelter/register.html'
    # success_url = reverse_lazy('exit_register')

    # def form_valid(self, form):
    #     messages.success(self.request, 'El centro ha sido registrado existosamente. La aprobación está pendiente')
    #     return super().form_valid(form)

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