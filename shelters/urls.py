from django.urls import path
from .views import landing_page
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', landing_page, name='landing_page'),

    # Shelter
    path('shelter/register/', views.RegisterShelterView.as_view(), name='register_shelter'),
    path('shelter/register-exit/', TemplateView.as_view(template_name='shelter/exit_register.html'), name='exit_register'),
    path('shelter/<int:pk>/', views.ShelterView.as_view(), name='view_shelter'),
    path('shelter/edit/<int:pk>/', views.UpdateShelterView.as_view(), name='edit_shelter'),
    path('shelter/delete/<int:pk>/', views.DeleteShelterView.as_view(), name='delete_shelter')
]