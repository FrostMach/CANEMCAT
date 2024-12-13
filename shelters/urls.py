from django.urls import path
from shelters import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [   
    path('crear/', views.AnimalCreateView.as_view(), name='animals-create'),
    path('editar/<int:pk>/', views.AnimalUpdateView.as_view(), name='animals-update'),
    path('eliminar/<int:pk>/', views.AnimalDeleteView.as_view(), name='animals-delete'),
    path('lista/', views.AnimalListView.as_view(), name='animals-list'),
    path('detalles/<int:pk>/', views.AnimalDetailView.as_view(), name='animals-detail'),
    path('shelters/confirmacion_solicitud/',views.confirm_view, name='solicitud_adopcion_confirm'),
    path('shelters/', views.ShelterList.as_view(), name='shelter_list'),
    path('shelter/register/', views.register_shelter, name='register_shelter'),
    path('shelter/<int:pk>/', views.ShelterView.as_view(), name='view_shelter'),
    path('shelter/edit/<int:pk>/', views.UpdateShelterView.as_view(), name='edit_shelter'),
    path('shelter/delete/<int:pk>/', views.DeleteShelterView.as_view(), name='delete_shelter'),
    path('shelter/<int:shelter_id>/approval/', views.shelter_approval, name='shelter_approval'),
    path('api/nearby-shelters/', views.nearby_shelters, name='nearby_shelters'),
    path('api/shelter-postal-code/', views.shelters_by_postal_code, name='shelter_postal_center'),
    path('shelter/nearby/', views.map_view, name='map'),
    path('lab/', views.landing_page2, name='lab'),
    path('lista_animales/', views.AnimalShelterListView.as_view(), name='animal_list'),
    path('shelter/animal/<int:animal_id>/adoptar/', views.adoption_application_view, name='adoption_application_create'),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)