from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ShelterWorkerProfile, AdopterProfile, News

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'full_name', 'phone_number', 'birth_date', 'profile_picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('User Type', {'fields': ('user_type',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'full_name', 'user_type', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'full_name')
    ordering = ('email',)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'image')  # Los campos que se mostrarán en la lista de noticias
    search_fields = ('title', 'content')  # Permite buscar por título o contenido
    list_filter = ('created_at',)  # Filtros para ordenar por fecha de creación

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ShelterWorkerProfile)
admin.site.register(AdopterProfile)
admin.site.register(News, NewsAdmin)

