from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from shelters.models import Animal, Shelter
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
        ('admin', 'Administrador'),
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
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
    shelter = models.ForeignKey(Shelter, on_delete=models.SET_NULL, null=True, blank=True, related_name='workers')
    position = models.CharField(max_length=100, blank=True, null=True, default='Empleado')

    def __str__(self):
        return f"{self.user.full_name} - {self.shelter.name if self.shelter else 'Sin protectora'}"
    
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

class CompatibilityTest(models.Model):
    PET_CHOICES = [
        ('dog', 'Perro'),
        ('cat', 'Gato')
    ]
    
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    pet_type = models.CharField(max_length=3, choices=PET_CHOICES)
    
    # Preguntas relacionadas con el perro
    dog_age_preference = models.CharField(max_length=20)
    dog_coat_type = models.CharField(max_length=20)
    dog_character = models.CharField(max_length=20)
    dog_energy_level = models.CharField(max_length=20)
    dog_other_pets = models.CharField(max_length=20)
    
    # Preguntas relacionadas con el gato
    cat_age_preference = models.CharField(max_length=20)
    cat_coat_type = models.CharField(max_length=20)
    cat_character = models.CharField(max_length=20)
    cat_energy_level = models.CharField(max_length=20)
    cat_other_pets = models.CharField(max_length=20)

    def __str__(self):
        return f'Test de compatibilidad de {self.user.username} con {self.pet_type}'


# Wishlist model
class Wishlist(models.Model):
    INTERACTION_TYPE = [
        ('view', 'View'), 
        ('favorite', 'Favorite'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    interaction_type = models.CharField(blank=True, null=True, max_length=50, choices=INTERACTION_TYPE)

    def __str__(self):
        return f"{self.user.full_name} - {self.animal.name}"

    class Meta:
        db_table = 'wishlist'  # Custom table name in the database
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'animal', 'interaction_type'],
                name='unique_user_animal_interaction'
            )
        ]
        
class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    original_url = models.URLField(blank=True, null=True)  # Campo para el enlace

    def __str__(self):
        return self.title
    