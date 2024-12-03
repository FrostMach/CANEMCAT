from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from shelters.models import Animal

class Intent(models.Model):
    name = models.CharField(max_length=100)
    patterns = models.JSONField(null=True, blank=True)
    responses = models.JSONField(null=True, blank=True)
    def get_patterns(self):
        """ Convierte los patrones en una lista de palabras claves """
        return [pattern.strip() for pattern in self.patterns.split(',')]

    def get_responses(self):
        """ Convierte las respuestas en una lista de respuestas """
        return [response.strip() for response in self.responses.split(',')]

    def get_response(self, user_message):
        """ Devuelve la respuesta adecuada basado en el mensaje del usuario """
        patterns = self.get_patterns()

        # Recorre todos los patrones para encontrar una coincidencia
        for pattern in patterns:
            if pattern.lower() in user_message.lower():
                return self.get_responses()[0]  # O puedes elegir una respuesta aleatoria aquí

        return None  # Si no hay coincidencia

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


class Interaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  null=True, blank=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interaction {self.user} at {self.timestamp}"

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
        

        

