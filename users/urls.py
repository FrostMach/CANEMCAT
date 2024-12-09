from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static
from .views import landing_page,email_confirmation

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset, name='password_reset_confirm'),
    path('password_reset_email/', views.password_reset, name='password_reset_email'),
    path('email_confirmation/', email_confirmation, name='email_confirmation'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('logout/', views.logout_view, name='logout'),  
    path('wishlist/', views.wishlist_list, name='wishlist_list'),
    # path('<int:animal_id>/add_wishlist/', views.wishlist_add, name='wishlist_add'),
    path('wishlist/add/', views.wishlist_add, name='wishlist_add'),
    path('<int:wishlist_id>/remove_wishlist/', views.wishlist_remove, name='wishlist_remove'),  
    # path('animals/recommendations/', views.recommend_animals, name='recommended_animals'),
    # path('animals/evaluate', views.evaluate_system, name='evaluate_system'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    # path('dashboard/recommendations/', views.get_recommendations, name='get_recommendations'),
    # path('animals/<int:animal_id>/interact/<str:interaction_type>/', views.record_interaction, name='record_interaction'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
