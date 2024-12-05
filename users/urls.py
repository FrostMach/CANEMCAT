from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static
from .views import landing_page,email_confirmation,canemtest_view



from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('email_confirmation/', email_confirmation, name='email_confirmation'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('logout/', views.logout_view, name='logout'),
    path('canem_test/', canemtest_view, name='canem_test'),
    path('dog_test/', views.DogTestView.as_view(), name='dog_test'),    
    path('cat_test/', views.CatTestView.as_view(), name='cat_test'),   
    path('resultado/', views.resultado_test, name='resultado_test'),  # URL para los resultados


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

