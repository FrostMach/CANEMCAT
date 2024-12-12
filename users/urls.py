from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static
from .views import landing_page,email_confirmation,canem_test
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
    # path('<int:animal_id>/add_wishlist/', views.wishlist_add, name='wishlist_add'),
    path('wishlist/add/', views.wishlist_add, name='wishlist_add'),
    path('<int:wishlist_id>/remove_wishlist/', views.wishlist_remove, name='wishlist_remove'),
    path('canem_test/', views.canem_test, name='canem_test'),  # Vista para seleccionar la especie
    path('dog_test/', views.DogTestView.as_view(), name='dog_test'),    
    path('cat_test/', views.CatTestView.as_view(), name='cat_test'),   
    path('resultado/', views.resultado_test, name='resultado_test'),
    path('canemscan/', views.canem_scan, name='canemscan'),
    path('canemscan/upload/', views.upload_image, name='upload_image'),
    path('canemscan/compare/', views.compare_images, name='compare_images'),   
    # path('animals/recommendations/', views.recommend_animals, name='recommended_animals'),
    # path('animals/evaluate', views.evaluate_system, name='evaluate_system'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    # path('dashboard/recommendations/', views.get_recommendations, name='get_recommendations'),
    # path('animals/<int:animal_id>/interact/<str:interaction_type>/', views.record_interaction, name='record_interaction'),    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
