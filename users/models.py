from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    def __str__(self):
        return self.username
from django.db import models

# Create your models here.
from users.models import CustomUser
# Create your models here.
from enum import Enum

class StatusEnum(Enum):
    PENDING = 'P', 'Pendiente'
    APPROVED = 'A', 'Aprobada'
    DENIED = 'D', 'Denegada'
    
class Animal(models.Model):
    SPECIES = [
        ('perro','Perro'),
        ('gato','Gato')
    ]
    ADOPTION_STATUS = [
        ('disponible','Disponible'),
        ('reservado','Reservado'),
        ('adoptado','Adoptado')
    ]
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    species = models.CharField(max_length=10,choices=SPECIES)
    description = models.TextField()
    image = models.ImageField(upload_to='animals/')
    adoption_status = models.CharField(max_length=10,choices=ADOPTION_STATUS,default='disponible')
    
    def __str__(self):
        return self.name
    

class Shelter(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    address = models.CharField(max_length=100, verbose_name='Dirección')
    telephone = models.CharField(max_length=12, verbose_name='Teléfono')
    email = models.EmailField(max_length=100, verbose_name='Correo electrónico')
    accreditation_file = models.FileField(blank=True, null=True, upload_to='uploads/', verbose_name='Documento acreditativo')
    accreditation_status = models.BooleanField(default=True, verbose_name='Estado de acreditación')
    register_date = models.DateField(blank=True, null=True, verbose_name='Fecha de registro')
    status = models.BooleanField(verbose_name='Estado', blank=True, null=True)

    def str(self):
        return f'{self.name}'
class AdoptionApplication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True)
    center = models.ForeignKey(Shelter, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=1,
        choices=[(tag.value[0], tag.value[1]) for tag in StatusEnum],
        default=StatusEnum.PENDING.value[0]
    )
    application_date = models.DateField()
    def __str__(self):
        return f"Solicitud de adopción de {self.user.full_name} para {self.animal}"



