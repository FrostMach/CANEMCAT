from django.core.management.base import BaseCommand
from shelters.models import Animal
from users.utils.image_processing import extract_features
import numpy as np

class Command(BaseCommand):
    help = 'Preprocesa y guarda características de imágenes para los animales'

    def handle(self, *args, **kwargs):
        animals = Animal.objects.filter(features__isnull=True).exclude(image='')
        for animal in animals:
            self.stdout.write(f'Procesando {animal.name} ({animal.species})...')
            try:
                features = extract_features(animal.image.path)
                animal.features = np.array(features).tobytes()
                animal.save()
                self.stdout.write(f'Características guardadas para {animal.name}.')
            except Exception as e:
                self.stdout.write(f'Error procesando {animal.name}: {e}')
