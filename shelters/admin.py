from django.contrib import admin
from .models import Shelter

# Register your models here.
class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'telephone', 'status')
    list_filter = ('status',)
    actions = ['approve_accreditation', 'reject_accreditation']

    def approve_accreditation(self, request, queryset):
        queryset.update(status=True)
    approve_accreditation.short_description = "Aprobar documentos de acreditación"

    def reject_accreditation(self, request, queryset):
        queryset.update(status=False)
    reject_accreditation.short_description = "Rechazar documentos de acreditación"

admin.site.register(Shelter, ShelterAdmin)