from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static
from .views import RecommendationView, landing_page,email_confirmation,canem_test
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
    path('profile/edit/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('worker/<int:pk>/', views.ProfileWorkerView.as_view(), name='profile_worker'),
    path('worker/edit/<int:pk>/', views.ProfileWorkerUpdateView.as_view(), name='profile_worker_edit'),
    path('logout/', views.logout_view, name='logout'),
    path('wishlist/', views.wishlist_list, name='wishlist_list'),
    path('wishlist/add/', views.wishlist_add, name='wishlist_add'),
    path('<int:wishlist_id>/remove_wishlist/', views.wishlist_remove, name='wishlist_remove'),
    path('canem_test/', views.canem_test, name='canem_test'),  # Vista para seleccionar la especie
    path('dog_test/', views.DogTestView.as_view(), name='dog_test'),
    path('cat_test/', views.CatTestView.as_view(), name='cat_test'),
    path('resultado/', views.resultado_test, name='resultado_test'),
    path('canemscan/', views.canem_scan, name='canemscan'),
    path('canemscan/upload/', views.upload_image, name='upload_image'),
    path('canemscan/compare/', views.compare_images, name='compare_images'),
    path('guardar_animal/', views.guardar_animal, name='guardar_animal'),   
    path('shelters/confirmar_adopcion/<int:animal_id>/', views.adoption_application_view, name='confirm_adoption'),
    path('adoption/applications/', views.adoption_application_list, name='adoption_application_list'),
    path('shelters/error_de_tipo_usuario/', views.error_user_type, name='error_user_type'),
    path('adoption-applications-shelterworker/', views.adoption_application_list_shelterworker, name='adoption_application_list_shelterworker'),
    path('adoption-application/update/<int:application_id>/', views.update_adoption_application, name='update_adoption_application'),
    path('animals/recommendations/', RecommendationView.as_view(), name='recommendations'),
    path('shelter/<int:shelter_id>/add_worker/', views.add_shelter_worker, name='add-shelter-worker'),
    path('shelter/<int:shelter_id>/workers/', views.shelter_workers, name='shelter_workers'),
    path('worker/<int:worker_id>/remove/<int:shelter_id>/', views.remove_worker, name='remove-worker'),
        
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)