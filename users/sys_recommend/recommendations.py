import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

SPECIES_MAPPING = {'perro': 1, 'gato': 2}
SIZE_MAPPING = {'grande': 3, 'mediano': 2, 'pequeño': 1}
PERSONALITY_MAPPING = {'sociable': 3, 'protector': 2, 'independiente': 1}
ENERGY_MAPPING = {'activo': 3, 'moderado': 2, 'tranquilo': 1}
FUR_MAPPING = {'largo': 2, 'corto': 1}
SEX_MAPPING = {'macho': 1, 'hembra': 2}

def encode_features(df):
    """Convierte características categóricas en valores numéricos."""
    df['species'] = df['species'].map(SPECIES_MAPPING).fillna(0)
    df['size'] = df['size'].map(SIZE_MAPPING).fillna(0)
    df['personality'] = df['personality'].map(PERSONALITY_MAPPING).fillna(0)
    df['energy'] = df['energy'].map(ENERGY_MAPPING).fillna(0)
    df['fur'] = df['fur'].map(FUR_MAPPING).fillna(0)
    df['sex'] = df['sex'].map(SEX_MAPPING).fillna(0)
    return df

def load_csv_data():
    animal_data_path = os.path.join("dynamic_data", "animal_data.csv")
    wishlist_data_path = os.path.join("dynamic_data", "wishlist_data.csv")

    animals = pd.read_csv(animal_data_path)
    wishlist = pd.read_csv(wishlist_data_path)

    if 'image' not in animals.columns:
        raise ValueError("El archivo CSV no tiene la columna 'image'")

    animals['image'] = animals['image'].apply(lambda x: os.path.join('media', x))
    
    return animals, wishlist

def recommend_from_csv(user_id, top_n=5):
    animals, wishlist = load_csv_data()
    
    # Verificar que los datos de animales estén disponibles
    if animals.empty:
        return {"error": "No hay datos de animales disponibles."}
    
    # Codificar características de los animales
    animals = encode_features(animals)
    
    # Filtrar los favoritos del usuario
    user_favorites = wishlist[wishlist['user_id'] == user_id]
    favorite_animal_ids = user_favorites['animal_id'].tolist()

    # Obtener los animales favoritos
    favorite_animals = animals[animals['id'].isin(favorite_animal_ids)]
    
    if favorite_animals.empty:
        # Si el usuario no tiene favoritos, devolver animales aleatorios
        return animals.sample(n=min(top_n, len(animals)))

    # Generar vectores de características para animales favoritos
    feature_columns = ['species', 'size', 'personality', 'energy', 'fur', 'sex']
    favorite_vectors = favorite_animals[feature_columns].values.astype(float)
    
    # Calcular el vector promedio
    if favorite_vectors.shape[0] == 0:
        return {"error": "No se pudieron calcular vectores para favoritos."}
    
    average_vector = np.mean(favorite_vectors, axis=0)

    # Filtrar animales disponibles
    available_animals = animals[animals['adoption_status'] == 'disponible']
    if available_animals.empty:
        # Si no hay animales disponibles, devolver animales aleatorios
        return animals.sample(n=min(top_n, len(animals)))

    # Generar vectores para animales disponibles
    available_vectors = available_animals[feature_columns].values.astype(float)
    if available_vectors.shape[0] == 0:
        return {"error": "No se pudieron calcular vectores para animales disponibles."}

    # Calcular similitudes
    similarities = cosine_similarity([average_vector], available_vectors)[0]
    available_animals['similarity'] = similarities

    # Ordenar y seleccionar los más similares
    recommendations = available_animals.sort_values('similarity', ascending=False).head(top_n)

    return recommendations
