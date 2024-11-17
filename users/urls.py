from django.urls import path,include
from users import views
from django.conf import settings
from django.conf.urls.static import static
from .views import landing_page,confirm_view,AdoptionApplicationCreateView
urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('crear/', views.AnimalCreateView.as_view(), name='animals-create'),
    path('editar/<int:pk>/', views.AnimalUpdateView.as_view(), name='animals-update'),
    path('eliminar/<int:pk>/', views.AnimalDeleteView.as_view(), name='animals-delete'),
    path('lista/', views.AnimalListView.as_view(), name='animals-list'),
    path('shelters/solicitud_adopcion/', AdoptionApplicationCreateView.as_view(), name='solicitud_adopcion_create'),
    path('shelters/confirmacion_solicitud/',confirm_view, name='solicitud_adopcion_confirm'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),

