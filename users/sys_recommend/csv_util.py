import csv

import pandas as pd
from ..models import Animal, Wishlist
import os

def export_data_to_csv():
    file_path = os.path.join("dynamic_data", "animal_data.csv")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Escribe la cabecera
        writer.writerow([
            'id', 'name', 'species', 'size', 'personality',
            'energy', 'fur', 'sex', 'adoption_status', 'description', 'image'
        ])

        # Escribe los datos de los animales
        for animal in Animal.objects.all():
            writer.writerow([
                animal.id, animal.name, animal.species, animal.size,
                animal.personality, animal.energy, animal.fur,
                animal.sex, animal.adoption_status, animal.description, animal.image.url if animal.image else None
            ])

    print(f"CSV actualizado en {file_path}")

def export_wishlist_to_csv():
    file_path = os.path.join("dynamic_data", "wishlist_data.csv")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Escribe la cabecera
        writer.writerow(['user_id', 'animal_id', 'interaction_type'])

        # Escribe los datos de las interacciones
        for wishlist in Wishlist.objects.all():
            writer.writerow([wishlist.user.id, wishlist.animal.id, wishlist.interaction_type])

    print(f"CSV de wishlist actualizado en {file_path}")

def generate_animal_data():
    # Recupera todos los datos de animales
    file_path = os.path.join("dynamic_data", "animal_data.csv")

    # Asegúrate de que el directorio exista
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Recuperar los datos de los animales
    animals = Animal.objects.all().values(
        'id', 'name', 'species', 'sex', 'age', 'size', 'personality',
        'energy', 'fur', 'description', 'adoption_status', 'image'
    )

    # Si no hay animales, devolver un mensaje de error
    if not animals:
        raise ValueError("No hay animales disponibles para exportar")

    # Crear el DataFrame a partir de los datos
    df = pd.DataFrame(list(animals))

    # Guardar los datos en el archivo CSV
    df.to_csv(file_path, index=False, encoding='utf-8')

    print(f"Archivo animal_data.csv generado en {file_path}")