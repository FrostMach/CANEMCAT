from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from shelters.models import Animal
import re
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

def validate_phone_number(value):
    pattern = r'^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
    if not re.match(pattern, value):
        raise ValidationError(f"El número de teléfono {value} no es válido.")

def validate_email(value):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, value):
        raise ValidationError(f"El correo electrónico {value} no es válido.")

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('adopter', 'Adopter'),  # Persona que adopta
        ('worker', 'Shelter Worker'),  # Trabajador de protectora
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=9, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='adopter')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
    
class ShelterWorkerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='worker_profile')
    shelter_name = models.CharField(max_length=255)
    position = models.CharField(max_length=100, blank=True, null=True, default='Empleado')

    def __str__(self):
        return f"{self.user.full_name} - {self.shelter_name}"
    
class AdopterProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='adopter_profile')
    adoption_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.full_name    

class Test(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)

class Questions(models.Model):
    question_text = models.CharField(max_length=255)

class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='questions')

# Wishlist model
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlists')
    animals = models.ManyToManyField(Animal, related_name='wishlists')
    class Meta:
        db_table = 'wishlist'  # Custom table name in the database
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
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
        

        
