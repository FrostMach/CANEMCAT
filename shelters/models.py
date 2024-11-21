from django.db import models

# Create your models here.
class Shelter(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    address = models.CharField(max_length=100, verbose_name='Dirección')
    telephone = models.CharField(max_length=12, verbose_name='Teléfono')
    email = models.EmailField(max_length=100, verbose_name='Correo electrónico')
    accreditation_file = models.FileField(blank=True, null=True, upload_to='files/', verbose_name='Documento acreditativo')
    accreditation_status = models.BooleanField(default=True, verbose_name='Estado de acreditación')
    register_date = models.DateField(blank=True, null=True, verbose_name='Fecha de registro')
    status = models.BooleanField(verbose_name='Estado', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'