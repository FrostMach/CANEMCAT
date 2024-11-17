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
    
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    species = models.CharField(max_length=10, choices=SPECIES)
    description = models.TextField()
    image = models.ImageField(upload_to='animals/')
    adoption_status = models.CharField(max_length=10, choices=ADOPTION_STATUS, default='disponible')

    def __str__(self):
        return self.name
    
    #shelter = models.ForeignKey('Shelter', on_delete=models.CASCADE, related_name='animals')
    #wishlist = models.ManyToManyField('Wishlist', blank=True, related_name='animals')
    #request = models.ManyToManyField('Request', blank=True, related_name='animals')