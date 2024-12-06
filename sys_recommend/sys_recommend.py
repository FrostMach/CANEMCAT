import numpy as np
import pandas as pd
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from ..users.models import Animal, Wishlist

def recommend_pets(user_id, top_n = 5):
    animals = Animal.objects.all().values('id', 'age', 'species', 'description', 'adoption_status', 'image')
    df_animals = pd.DataFrame(animals)

    if df_animals.empty:
        return pd.DataFrame()

    df_animals['features'] = df_animals['species'] + ' ' + df_animals['description'] + '' + df_animals['adoption_status']

    vectorizer = TfidfVectorizer()
    feature_matrix = vectorizer.fit_transform(df_animals['features'])
    cosine_sim = cosine_similarity(feature_matrix, feature_matrix)

    interactions = Wishlist.objects.filter(user_id= user_id, interaction_type__in=['view', 'favorite'])
    pet_ids = [interaction.animal for interaction in interactions]

    if not pet_ids:
        return pd.DataFrame()
    
    try:
        user_sim_scores = cosine_sim[pet_ids].mean(axis=0)
        recommend_indices = user_sim_scores.argsor()[-top_n:][::-1]
        return df_animals.iloc[recommend_indices]
    
    except Exception as e:
        print(f'Error calculando recomendaciones: {e}')
        return pd.DataFrame()
    
    # user_prefs = Wishlist.objects.filter(user = user_id)

    # pets = Animal.objects.all()
    # df_pets = pd.DataFrame(list(pets.values()))

    # df_pets['features'] = df_pets.apply(lambda x: f'{x['species']} {x['age']} {x['description']} {x['adoption_status']}', axis=1)

    # vectorizer = TfidfVectorizer()
    # matrix_vector = vectorizer.fit_transform(df_pets['features'])

    # cosine_sim = cosine_similarity(matrix_vector)

    # user_pets = [pref.animal.id for pref in user_prefs]

    # sim_scores = []
    # for pet_id in user_pets:
    #     sim_scores.extend(list(enumerate(cosine_sim[pet_id-1])))

    # sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # pet_indices = [i[0] for i in sim_scores if i[0]+1 not in user_pets]

    # return df_pets.iloc[pet_indices[:5]]
