from django.db import models
from enum import Enum
from datetime import date
from django.core.exceptions import ValidationError
from django.conf import settings

class Shelter(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    address = models.CharField(max_length=100, verbose_name='Dirección')
    telephone = models.CharField(max_length=12, verbose_name='Teléfono')
    email = models.EmailField(max_length=100, verbose_name='Correo electrónico')
    accreditation_file = models.FileField(blank=True, null=True, upload_to='files/', verbose_name='Documento acreditativo')
    register_date = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='Fecha de registro')
    status = models.BooleanField(verbose_name='Estado', blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True, verbose_name='Latitud')
    longitude = models.FloatField(blank=True, null=True, verbose_name='Longitud')
    postal_code = models.CharField(blank=True, null=True, max_length=10, verbose_name='Código Postal')

    def __str__(self):
        return f'{self.name}'       

class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events", null=True)    
    description = models.TextField(default='')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    color = models.CharField(max_length=7, default='#FFFFFF')  # El color en formato #hex

    def __str__(self):
        return f"{self.description} ({self.date})"


class StatusEnum(Enum):
    PENDING = 'P', 'Pendiente'
    APPROVED = 'A', 'Aprobada'
    DENIED = 'D', 'Denegada'

class Animal(models.Model):
    SPECIES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
    ]
    ADOPTION_STATUS = [
        ('disponible', 'Disponible'),
        ('reservado', 'Reservado'),
        ('adoptado', 'Adoptado'),
    ]
    SIZE = [
        ('grande', 'Grande'),
        ('mediano', 'Mediano'),
        ('pequeño', 'Pequeño'),
    ]
    PERSONALITY = [
        ('sociable', 'Sociable'),
        ('protector', 'Protector'),
        ('independiente', 'Independiente'),
    ]
    ENERGY = [
        ('activo', 'Activo'),
        ('moderado', 'Moderado'),
        ('tranquilo', 'Tranquilo'),
    ]
    FUR = [
        ('largo', 'Largo'),
        ('corto', 'Corto'),
    ]
    SEX = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]
    name = models.CharField(max_length=100, verbose_name='Nombre')
    species = models.CharField(max_length=10, choices=SPECIES, verbose_name='Especie')
    sex = models.CharField(max_length=10, choices=SEX, default='Macho')
    age = models.PositiveIntegerField()
    size = models.CharField(max_length=10, choices=SIZE)
    personality = models.CharField(max_length=15, choices=PERSONALITY)
    energy = models.CharField(max_length=10, choices=ENERGY)
    fur = models.CharField(max_length=10, choices=FUR)
    description = models.TextField()
    image = models.ImageField(upload_to='animals/')
    adoption_status = models.CharField(max_length=10, choices=ADOPTION_STATUS, default='Disponible')
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='animals', verbose_name='Protectora',null=True)
    features = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        """
        Validación personalizada: Si el animal es un gato, size no debe ser obligatorio.
        """
        if self.species == 'perro' and not self.size:
            raise ValidationError({'size': 'El tamaño es obligatorio para los perros.'})

class StatusEnum(Enum):
    PENDING = 'P', 'Pendiente'
    APPROVED = 'A', 'Aprobada'
    DENIED = 'D', 'Denegada'
    
class AdoptionApplication(models.Model):
    user = models.ForeignKey('users.AdopterProfile', on_delete=models.CASCADE, default=1)
    animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True)
    shelter = models.ForeignKey(Shelter, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=1,
        choices=[(tag.value[0], tag.value[1]) for tag in StatusEnum],
        default=StatusEnum.PENDING.value[0]
    )
    application_date = models.DateField(default=date.today)
    def __str__(self):
        return f"Solicitud de adopción de {self.user.full_name} para {self.animal}"
    
    from django.db import models

class Item(models.Model):
    CATEGORY = [
        ('alimentos', 'Alimentos'),
        ('medicamentos_vacunas', 'Medicamentos y Vacunas'),
        ('otros', 'Otros'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nombre del producto")
    category = models.CharField(max_length=20, choices=CATEGORY, verbose_name="Categoría")
    quantity = models.PositiveIntegerField(verbose_name="Cantidad")
    description = models.TextField(blank=True, verbose_name="Descripción")
    expiration_date = models.DateField(
        null=True, blank=True, verbose_name="Fecha de caducidad"
    )
    no_expiration = models.BooleanField(
        default=False, verbose_name="Sin fecha de caducidad"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    def __str__(self):
        return self.name
