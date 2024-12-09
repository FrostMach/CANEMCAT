from django.http import JsonResponse
import numpy as np
import pandas as pd
# from tensorflow.keras.applications import ResNet50
# from tensorflow.keras.applications.resnet50 import preprocess_input
# from tensorflow.keras.preprocessing import image
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
from sklearn.model_selection import train_test_split
from ..models import Animal
from ..models import Wishlist
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# # def recommend_pets(user_id, top_n = 5):
#     animals = Animal.objects.all().values('id', 'age', 'species', 'description', 'adoption_status', 'image')
#     df_animals = pd.DataFrame(animals)

#     if df_animals.empty:
#         return pd.DataFrame()

#     df_animals['features'] = df_animals['species'] + ' ' + df_animals['description'] + '' + df_animals['adoption_status']

#     vectorizer = TfidfVectorizer()
#     feature_matrix = vectorizer.fit_transform(df_animals['features'])
#     cosine_sim = cosine_similarity(feature_matrix, feature_matrix)

#     interactions = Wishlist.objects.filter(user_id= user_id, interaction_type__in=['view', 'favorite'])
#     pet_ids = [interaction.animal for interaction in interactions]

#     if not pet_ids:
#         return pd.DataFrame()
    
#     try:
#         user_sim_scores = cosine_sim[pet_ids].mean(axis=0)
#         recommend_indices = user_sim_scores.argsor()[-top_n:][::-1]
#         return df_animals.iloc[recommend_indices]
    
#     except Exception as e:
#         print(f'Error calculando recomendaciones: {e}')
#         return pd.DataFrame()
    
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

# def preprocess_animal_features(animal):
#     features = [
#         1 if animal.species == 'perro' else 0,
#         1 if animal.species == 'gato' else 0,
#         1 if animal.size == 'grande' else 0,
#         1 if animal.size == 'mediano' else 0,
#         1 if animal.size == 'pequeño' else 0,
#         1 if animal.personality == 'sociable' else 0,
#         1 if animal.personality == 'protector' else 0,
#         1 if animal.personality == 'independiente' else 0,
#         1 if animal.energy == 'activo' else 0,
#         1 if animal.energy == 'moderado' else 0,
#         1 if animal.energy == 'tranquilo' else 0,
#         1 if animal.fur == 'corto' else 0,
#         1 if animal.fur == 'largo' else 0,
#         1 if animal.sex == 'macho' else 0,
#         1 if animal.sex == 'hembra' else 0
#     ]

#     return features

# def recommend_animals(user):
#     user_interactions = Wishlist.objects.filter(user=user, interaction_type='favorite')
#     favorite_animals = [item.animal for item in user_interactions]

#     favorite_features = np.array([animal.features for animal in favorite_animals])

#     all_animals = Animal.objects.filter(adoption_status='disponible')
#     all_features = np.array([animal.features for animal in all_animals])

#     similarities = cosine_similarity(favorite_features, all_features)

#     similar_animals = sorted(
#         zip(all_animals, similarities.max(axis=0)),
#         key=lambda x: x[1], reverse=True
#     )

#     return [animal for animal, _ in similar_animals[:5]]

def calculate_animal_similarities():
    animals = Animal.objects.filter(adoption_status='disponible')

    if not animals.exists():
        return pd.DataFrame()
    
    animal_data = pd.DataFrame.from_records(animals.values(
        'id', 'species', 'size', 'personality', 'energy', 'fur', 'age'
    ))

    categorical_features = ['species', 'size', 'personality', 'energy', 'fur']
    encoder = OneHotEncoder()
    encoded_features = encoder.fit_transform(animal_data[categorical_features]).toarray()

    scaler = StandardScaler()
    normalized_age = scaler.fit_transform(animal_data['age'])

    feature_matrix = pd.concat([pd.DataFrame(encoded_features), pd.DataFrame(normalized_age, columns=['age_normalized'])], axis=1)
    similarity_matrix = cosine_similarity(feature_matrix)

    similarity_df = pd.DataFrame(similarity_matrix, index=animal_data['id'], columns=animal_data['id'])

    return similarity_df

def get_user_recommendations(user):
    similarity_df = calculate_animal_similarities()

    if similarity_df.empty:
        return Animal.objects.none()
    
    interactions = Wishlist.objects.filter(user=user).values('animal_id', 'interaction_type')

    if not interactions.exists():
        return Animal.objects.none()
    
    weights = {
        'favorite': 1,
        'view': 0.2
    }
    weighted_scores = {}

    for interaction in interactions:
        animal_id = interaction['animal_id']
        interaction_type = interaction['interaction_type']

        if animal_id in similarity_df.index:
            weigth = weights.get(interaction_type, 0)
            similarity_scores = similarity_df.loc[animal_id] * weigth

            for related_id, score in similarity_scores.items():
                weighted_scores[related_id] = weighted_scores.get(related_id, 0) + score

    recommended_animal_ids = sorted(weighted_scores, key=weighted_scores.get, reverse=True)
    
    user_animal_ids = [interaction['animal_id'] for interaction in interactions]
    recommended_animal_ids = [aid for aid in recommended_animal_ids if aid not in user_animal_ids][:5]

    return Animal.objects.filter(id__in=recommended_animal_ids, adoption_status='disponible')

    # interactions = Wishlist.objects.values('user_id', 'animal_id', 'interaction_type')
    
    # if not interactions.exists():
    #     return []  # Si no hay datos, retornar lista vacía
    
    # # Convertir interacciones a DataFrame
    # df = pd.DataFrame.from_records(interactions)
    # df['user_id'] = df['user_id'].astype(int)
    # df['animal_id'] = df['animal_id'].astype(int)
    
    # # Crear matriz de interacciones (usuarios vs animales)
    # interaction_matrix = df.pivot_table(
    #     index='user_id', columns='animal_id', 
    #     aggfunc='size', fill_value=0
    # )
    # interaction_matrix = interaction_matrix.astype(float)  # Asegurar valores numéricos
    
    # if interaction_matrix.empty:
    #     return []  # Si la matriz está vacía, no hay recomendaciones
    
    # # Eliminar columnas con valores constantes
    # interaction_matrix = interaction_matrix.loc[:, (interaction_matrix != 0).any(axis=0)]
    
    # if user.id not in interaction_matrix.index:
    #     return []  # Si el usuario no tiene interacciones, no puede haber recomendaciones
    
    # # Calcular la similitud entre usuarios
    # similarity_matrix = interaction_matrix.corr(method='pearson')
    
    # # Ordenar usuarios similares al usuario actual
    # similar_users = similarity_matrix[user.id].drop(user.id).sort_values(ascending=False)
    
    # if similar_users.empty:
    #     return []  # Si no hay usuarios similares, retornar lista vacía
    
    # # Seleccionar los animales vistos o favoritos por usuarios similares
    # similar_user_ids = similar_users.index.tolist()
    # recommendations = (
    #     Wishlist.objects.filter(user_id__in=similar_user_ids)
    #     .exclude(animal_id__in=interaction_matrix.loc[user.id][interaction_matrix.loc[user.id] > 0].index)  # Excluir animales ya vistos por el usuario
    #     .values('animal_id')
    #     .annotate(weight=Count('interaction_type'))  # Ponderar según la cantidad de interacciones
    #     .order_by('-weight')  # Ordenar por relevancia
    # )
    
    # # Obtener los IDs de animales recomendados
    # recommended_animal_ids = [rec['animal_id'] for rec in recommendations]
    
    # # Recuperar instancias de los animales desde la base de datos
    # recommended_animals = Animal.objects.filter(id__in=recommended_animal_ids, adoption_status='disponible')
    
    # return list(recommended_animals)
    # # interactions = 
    # # interaction_matrix = get_interaction_matrix()

    # # if user.id not in interaction_matrix.index:
    # #     return Animal.objects.none()
    
    # # user_vector = interaction_matrix.loc[user.id].values.reshape(1, -1)
    # # similarity = cosine_similarity(interaction_matrix, user_vector).flatten()
    # # similar_users = interaction_matrix.index[similarity.argsort()[::-1]]
    # # recommended_animals = set()

    # # for similar_user in similar_users:
    # #     if len(recommended_animals == 5):
    # #         break

    # #     user_animals = interaction_matrix.loc[similar_user][interaction_matrix.loc[similar_user]> 0].index
    # #     recommended_animals.update(user_animals)

    # # recommended_animals.difference_update(interaction_matrix.loc[user.id][interaction_matrix.loc[user.id]> 0].index)

    # # return Animal.objects.filter(id__in=recommended_animals)

# def svd_recommendations(user_id, interaction_matrix, top=5):
#     interaction_np = interaction_matrix.to_numpy()

#     U, sigma, Vt = svds(interaction_np, k=50)
#     sigma = np.diag(sigma)

#     predicted_ratings = np.dor(np.dot(U, sigma), Vt)
#     predictions_df = pd.DataFrame(predicted_ratings, index=interaction_matrix.index, columns=interaction_matrix.columns)

#     user_predictions = predictions_df.loc[user_id].sort_values(ascending=False)

#     user_interactions = interaction_matrix.loc[user_id]
#     recommended_animals = user_predictions[user_interactions == 0].head(top)

#     return recommended_animals.index.tolist()

# def split_interaction_data(interactions):
#     data = {
#         'user_id': [item.user.id for item in interactions],
#         'animal_id': [item.animal.id for item in interactions],
#         'interaction_type': [1 if item.interaction_type == 'favorite' else 0.2 for item in interactions],
#     }

#     df = pd.DataFrame(data)

#     train, test = train_test_split(df, test_size=0.2, random_state=42)
    
#     return train, test

# def precision_at_k(recommended, relevant, k=10):
#     recommended_k = recommended[:k]
#     relevant_set = set(relevant)
#     recommended_set = set(recommended_k)

#     return len(recommended_set & relevant_set) /k

# def recall_at_k(recommended, relevant, k=10):
#     recommended_k = recommended[:k]
#     relevant_set = set(relevant)
#     recommended_set = set(recommended_k)

#     return len(recommended_set & relevant_set) / len(relevant_set) if relevant_set else 0

# def evaluate_recommendations(interaction_matrix, test_data, method='user_based'):
#     precision_scores = []
#     recall_scores = []

#     for user_id in test_data['user_id'].unique():
#         relevant_animals = test_data[test_data['user_id'] == user_id]['animal_id'].tolist()

#         if method == 'user_based':
#             recommended = user_recommendations(user_id, interaction_matrix)
#         elif method == 'item_based':
#             recommended = item_recommendations(user_id, interaction_matrix)
#         else:
#             recommended = svd_recommendations(user_id, interaction_matrix)
        
#         precision = precision_at_k(recommended, relevant_animals)
#         recall = recall_at_k(recommended, relevant_animals)

#         precision_scores.append(precision)
#         recall_scores.append(recall)

#     return {
#         'precision@k':np.mean(precision_scores),
#         'recall@k':np.mean(recall_scores)
#     }

# def evaluate_system(request):
#     interactions = Wishlist.objects.all()

#     train_data, test_data = split_interaction_data(interactions)

#     train_interaction_matrix = get_interaction_matrix(train_data)

#     results_user_based = evaluate_recommendations(train_interaction_matrix, test_data, method='user_based')
#     results_item_based = evaluate_recommendations(train_interaction_matrix, test_data, method='item_based')
#     results_svd_based = evaluate_recommendations(train_interaction_matrix, test_data, method='svd_based')

#     return JsonResponse({
#         'user_based':results_user_based,
#         'item_based':results_item_based,
#         'svd_based':results_svd_based
#     })

# def user_recommendations(user_id, interaction_matrix, top=5):
#     sparse_matrix = csr_matrix(interaction_matrix.values)

#     user_similarity = cosine_similarity(sparse_matrix)
#     similarity_df = pd.DataFrame(user_similarity, index=interaction_matrix.index, columns=interaction_matrix.index)

#     similar_users = similarity_df[user_id].sort_values(ascending=False).iloc[1:]

#     similar_user_ids = similar_users.index
#     similar_user_interactions = interaction_matrix.loc[similar_user_ids].mean(axis=0)

#     user_interactions = interaction_matrix.loc[user_id]
#     recommend_animals = similar_user_interactions[user_interactions == 0].sort_values(ascending=False)

#     return recommend_animals.head(top).index.tolist()

# def item_recommendations(user_id, interaction_matrix, top=10):
#     sparse_matrix = csr_matrix(interaction_matrix.T.values)

#     item_similarity = cosine_similarity(sparse_matrix)
#     similarity_df = pd.DataFrame(item_similarity, index=interaction_matrix.columns, columns=interaction_matrix.columns)

#     user_interactions = interaction_matrix.loc[user_id]

#     scores = pd.Series(dtype=float)
#     for animal_id, interaction_score in user_interactions[user_interactions > 0].items():
#         similar_items = similarity_df[animal_id] * interaction_score
#         scores = scores.add(similar_items, fill_value=0)

#     scores = scores[user_interactions == 0]

#     return scores.sort_values(ascending=False).head(top).index.tolist()

# def recommend_animals(user, method='user_based', top=5):
#     interaction_matrix = get_interaction_matrix()

#     if user.id not in interaction_matrix.index:
#         return []
    
#     if method == 'user_based':
#         return user_recommendations(user.id, interaction_matrix, top)
#     elif method == 'item_based':
#         return item_recommendations(user.id, interaction_matrix, top)
#     else:
#         raise ValueError('Invalid recommendation method.')
    
# def create_interaction_matrix():
#     interactions = Wishlist.objects.all().values('user_id', 'animal_id', 'interaction_type')
#     data = pd.DataFrame(list(interactions))

#     if data.empty:
#         return pd.DataFrame()  # Devuelve un DataFrame vacío si no hay interacciones

#     # Convertir interacciones en una matriz de usuarios y animales
#     interaction_matrix = pd.pivot_table(
#         data, 
#         index='user_id', 
#         columns='animal_id', 
#         values='interaction_type', 
#         aggfunc='count', 
#         fill_value=0
#     )
#     return interaction_matrix
    
# def generate_user_based_recommendations(user_id, interaction_matrix):
#     if interaction_matrix.empty:
#         return []

#     # Asegurarnos de que el usuario esté en la matriz
#     if user_id not in interaction_matrix.index:
#         return []

#     # Similaridad del usuario con otros usuarios
#     user_similarities = cosine_similarity(interaction_matrix)
#     similarity_df = pd.DataFrame(user_similarities, index=interaction_matrix.index, columns=interaction_matrix.index)

#     # Recomendaciones basadas en usuarios similares
#     similar_users = similarity_df[user_id].sort_values(ascending=False).iloc[1:]  # Excluir al propio usuario
#     similar_user_ids = similar_users.index

#     # Obtener interacciones de usuarios similares
#     similar_user_interactions = interaction_matrix.loc[similar_user_ids].sum(axis=0)
    
#     # Filtrar animales ya interactuados por el usuario
#     user_interacted = interaction_matrix.loc[user_id]
#     recommendations = similar_user_interactions[user_interacted == 0]

#     # Ordenar y devolver los IDs de animales más recomendados
#     recommended_animal_ids = recommendations.sort_values(ascending=False).head(10).index
#     return recommended_animal_ids