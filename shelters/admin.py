from django.contrib import admin
from shelters.models import Shelter

# Register your models here.

    
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