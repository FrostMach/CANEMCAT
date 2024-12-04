from django.urls import path
from shelters import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
    
urlpatterns = [   
    path('crear/', views.AnimalCreateView.as_view(), name='animals-create'),
    path('editar/<int:pk>/', views.AnimalUpdateView.as_view(), name='animals-update'),
    path('<int:pk>/', views.AnimalDetailView.as_view(), name='animals-detail'),
    path('eliminar/<int:pk>/', views.AnimalDeleteView.as_view(), name='animals-delete'),
    path('lista/', views.AnimalListView.as_view(), name='animals-list'),
    path('shelters/solicitud_adopcion/', views.AdoptionApplicationCreateView.as_view(), name='solicitud_adopcion_create'),
    path('shelters/confirmacion_solicitud/',views.confirm_view, name='solicitud_adopcion_confirm'),
    path('shelters/', views.ShelterList.as_view(), name='shelter_list'),
    path('shelter/register/', views.RegisterShelterView.as_view(), name='register_shelter'),
    path('shelter/register-exit/', TemplateView.as_view(template_name='shelter/exit_register.html'), name='exit_register'),
    path('shelter/<int:pk>/', views.ShelterView.as_view(), name='view_shelter'),
    path('shelter/edit/<int:pk>/', views.UpdateShelterView.as_view(), name='edit_shelter'),
    path('shelter/delete/<int:pk>/', views.DeleteShelterView.as_view(), name='delete_shelter'),
    path('shelter/pending/<int:pk>/', views.CheckDocumentView.as_view(), name='check_pending'),
    path('shelter/pending', views.ShelterListPendingView.as_view(), name='shelter_list_pending'),
    path('api/nearby-shelters/', views.nearby_shelters, name='nearby_shelters'),
    path('api/shelter-postal-code/', views.shelters_by_postal_code, name='shelter_postal_center'),
    path('shelter/nearby/', views.map_view, name='map'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)