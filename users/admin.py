from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Shelter

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'full_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'full_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email', 'phone_number', 'address', 'birth_date', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )

# Registra el modelo en el admin
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'accreditation_status', 'register_date')
    list_filter = ('accreditation_status',)
    actions = ['accreditation_allow', 'accreditation_deny']

    
    def accreditation_allow(self, request, queryset):
        queryset.update(accreditation_status=True)

    # @admin.action(description='Accreditation Deny')
    # def accreditation_deny(self, request, queryset):
    #     queryset.update(accreditation_status='deny')