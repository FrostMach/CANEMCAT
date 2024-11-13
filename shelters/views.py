from django.shortcuts import render

# Create your views here.

# Vista para la landing page
def landing_page(request):
    return render(request, 'landing_page.html')