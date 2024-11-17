from django.urls import path
from django.views.generic import TemplateView
from users import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    
    # Shelter
    path('shelter/register/', views.RegisterShelterView.as_view(), name='register_shelter'),
    path('shelter/register-exit/', TemplateView.as_view(template_name='shelter/exit_register.html'), name='exit_register'),
    path('shelter/<int:pk>/', views.ShelterView.as_view(), name='view_shelter'),
    path('shelter/edit/<int:pk>/', views.UpdateShelterView.as_view(), name='edit_shelter'),
    path('shelter/delete/<int:pk>/', views.DeleteShelterView.as_view(), name='delete_shelter')
]
