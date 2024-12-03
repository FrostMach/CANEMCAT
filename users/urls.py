from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static
from .views import landing_page, chatbot_response
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('logout/', views.logout_view, name='logout'),    
    path('login/', views.login_view, name='login'),  # Ruta para iniciar sesión
    # path('chatbot/', views.chatbot_view, name='chatbot'),
    path('chatbot/', chatbot_response, name='chatbot_response'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


