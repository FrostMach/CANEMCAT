from django.contrib import admin
from .models import Shelter

# Register your models here.
admin.site.register(Shelter)
    
# @admin.register(Shelter)
# class ShelterAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'accreditation_status', 'register_date')
#     list_filter = ('accreditation_status',)
#     search_fields = ('name', 'email')
#     # actions = ['accreditation_allow', 'accreditation_deny']

    
#     def accreditation_allow(self, request, queryset):
#         queryset.update(accreditation_status=True)
#     accreditation_allow.short_description = 'Aprobar acreditación de los centros seleccionados'

#     actions = ['accreditation_allow']
#     # @admin.action(description='Accreditation Deny')
#     # def accreditation_deny(self, request, queryset):
#     #     queryset.update(accreditation_status='deny')