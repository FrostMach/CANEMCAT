from django.urls import path
from shelters import views
from django.conf import settings
from django.conf.urls.static import static
    
urlpatterns = [   
    path('crear/', views.AnimalCreateView.as_view(), name='animals-create'),
    path('editar/<int:pk>/', views.AnimalUpdateView.as_view(), name='animals-update'),
    path('eliminar/<int:pk>/', views.AnimalDeleteView.as_view(), name='animals-delete'),
    path('lista/', views.AnimalListView.as_view(), name='animals-list'),
    path('animals/<int:shelter_id>/', views.animals_list, name='animals-shelter-list'),
    path('detalles/<int:pk>/', views.AnimalDetailView.as_view(), name='animals-detail'),
    path('shelters/confirmacion_solicitud/',views.confirm_view, name='solicitud_adopcion_confirm'),
    path('shelters/', views.ShelterList.as_view(), name='shelter_list'),
    path('shelter/register/', views.ShelterRegistrationView.as_view(), name='register_shelter'),
    path('shelter/register/complete/<int:shelter_id>/', views.complete_shelter_registration, name='register_complete'),
    path('shelter/<int:pk>/', views.ShelterView.as_view(), name='view_shelter'),
    path('shelter/edit/<int:pk>/', views.UpdateShelterView.as_view(), name='edit_shelter'),
    path('shelter/delete/<int:pk>/', views.DeleteShelterView.as_view(), name='delete_shelter'),
    path('shelter/<int:shelter_id>/approval/', views.shelter_approval, name='shelter_approval'),
    path('api/nearby-shelters/', views.nearby_shelters, name='nearby_shelters'),
    path('api/shelter-postal-code/', views.shelters_by_postal_code, name='shelter_postal_center'),
    path('shelter/nearby/', views.map_view, name='map'),
    path('lab/', views.landing_page2, name='lab'),
    path('lista_animales/', views.AnimalShelterListView.as_view(), name='animal_list'),
    path('calendar/', views.index, name='calendar_view'),  # Ruta para mostrar el calendario
    path('get_events/', views.all_events, name='get_events'),  # Obtener los eventos en formato JSON
    path('add_event/', views.add_event, name='add_event'),  # Añadir un nuevo evento
    path('update/', views.update, name='update_event'),  # Actualizar un evento existente
    path('remove/', views.remove, name='remove_event'),  # Eliminar un evento
    path('inventario/', views.inventory_management, name='inventory_management'),
    path('inventario/add/', views.add_item, name='add_item'),
    path('inventario/edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('inventario/delete/<int:item_id>/', views.delete_item, name='delete_item'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)