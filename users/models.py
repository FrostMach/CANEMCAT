from django.db import models

# User model
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Campo adicional para saber si el usuario está activo
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Imagen de perfil (opcional)
    #class Meta:
    #    db_table = 'user'  # Custom table name in the database
    #    ordering = ['-registration_date']  # Default ordering: newest first
    #    verbose_name = 'User'
    #    verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.name} ({self.email})"

    # Método que devuelve el número de animales en la lista de deseos del usuario
    def wishlist_count(self):
        wishlist = Wishlist.objects.filter(user=self)
        return wishlist.first().animals.count() if wishlist.exists() else 0

# Animal model
class Animal(models.Model):
    OPCIONES = [('1', 'cat'), ('2', 'dog')]
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=1, choices=OPCIONES, default='1')  # '1' es para 'cat'
    age = models.IntegerField()
    # class Meta:
    #    db_table = 'animal'  # Custom table name in the database
    #    ordering = ['name']  # Default ordering by animal name
    #    verbose_name = 'Animal'
    #    verbose_name_plural = 'Animals'
    def __str__(self):
        return f"{self.name} ({self.get_species_display()})"

    # Método que devuelve una descripción completa del animal
    def full_description(self):
        return f"{self.name} is a {self.get_species_display()} of {self.age} years old."

    # Validación para el campo 'age', asegurando que sea positivo
    def clean(self):
        if self.age < 0:
            raise ValueError('Age must be a positive number.')


# Wishlist model
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
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

