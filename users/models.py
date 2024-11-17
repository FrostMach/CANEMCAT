from django.contrib.auth.models import AbstractUser
from django.db import models

# User model
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    def __str__(self):
        return self.username
# Animal model
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

# Wishlist model
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlists')
    animals = models.ManyToManyField(Animal, related_name='wishlists')
    # class Meta:
    #    db_table = 'wishlist'  # Custom table name in the database
    #    verbose_name = 'Wishlist'
    #    verbose_name_plural = 'Wishlists'
    def __str__(self):
        return f"Wishlist of {self.user.name}"

    # Método que verifica si un animal está en la lista de deseos
    def is_animal_in_wishlist(self, animal):
        return self.animals.filter(id=animal.id).exists()

    # Método que devuelve la cantidad de animales en la lista de deseos
    def animal_count(self):
        return self.animals.count()

    # Método que elimina un animal de la lista de deseos del usuario
    def remove_animal(self, animal):
        self.animals.remove(animal)

    # Método que agrega un animal a la lista de deseos del usuario
    def add_animal(self, animal):
        self.animals.add(animal)

