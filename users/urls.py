from django.urls import path,include
from users import views
from .views import landing_page,confirm_view,AdoptionApplicationCreateView
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('', landing_page, name='landing_page'),
    path('shelters/solicitud_adopcion/', AdoptionApplicationCreateView.as_view(), name='solicitud_adopcion_create'),
    path('shelters/confirmacion_solicitud/',confirm_view, name='solicitud_adopcion_confirm'),
]
