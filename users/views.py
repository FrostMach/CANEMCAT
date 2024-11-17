from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from users.models import Animal, Wishlist

# Create your views here.

# Vista para la landing page
def landing_page(request):
    return render(request, 'landing_page.html')


class AnimalDetailView(DetailView):
    model = Animal
    template_name = 'animals/details.html' 
    context_object_name = 'animal'  
    

class AddToWishlistView(ListView):
    
    model = Wishlist
    template_name = 'wish/list.html'
    context_object_name = 'add'

class RemoveFromWishlistView(ListView):
    
    model = Wishlist
    template_name = 'wish/list.html'
    context_object_name = 'remove'

