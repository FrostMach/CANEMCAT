from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomLoginView, CustomLogoutView, landing_page, login_view, logout_view
urlpatterns = [
    path('landing/', landing_page, name='landing_page'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

