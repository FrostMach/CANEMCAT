import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle
from django.utils import timezone
from django.contrib.auth import get_user_model


import sys
import os

# Establecer el entorno de Django para que funcione el import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))  # Agregar la carpeta del proyecto a sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'CANEMCAT.settings'

import django
django.setup()

from users.models import Interaction

# Inicializar el lematizador
lemmatizer = WordNetLemmatizer()

# Cargar los datos preprocesados y el modelo entrenado
with open('words.npy', 'rb') as f:
    words = np.load(f)

with open('classes.npy', 'rb') as f:
    classes = np.load(f)

with open('chatbot_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Cargar los datos de las intenciones
with open('chatbot_data.json','r', encoding='utf-8') as f:
    intents = json.load(f)

# Función para crear el "bag of words" para una frase de entrada
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(w.lower()) for w in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [1 if w in sentence_words else 0 for w in words]
    return np.array(bag)

# Función para obtener la respuesta del chatbot y registrar la interacción
def get_chatbot_response(user_input, user=None):
    # Convertir la frase del usuario en un "bag of words"
    bow_input = bow(user_input, words)
    
    # Predecir la clase (intención) de la frase del usuario
    prediction = model.predict([bow_input])
    predicted_class = prediction[0]
    
    # Buscar la respuesta correspondiente
    response = ""
    intent_name = classes[predicted_class]
    for intent in intents['intents']:
        if intent['intent'] == intent_name:
            response = np.random.choice(intent['responses'])
            break
    
    # Registrar la interacción en la base de datos
    if user:  # Si el usuario está autenticado
        Interaction.objects.create(user=user, user_message=user_input, bot_response=response)
    else:  # Si no hay un usuario autenticado (puede ser el caso de un chatbot sin sesión)
        Interaction.objects.create(user_message=user_input, bot_response=response)

    return response

# Probar el chatbot (esto sería el frontend o el script de prueba)
if __name__ == "__main__":
    while True:
        # Recibir la entrada del usuario
        user_input = input("Tú: ")
        
        # Aquí puedes simular un usuario autenticado si estás probando sin una sesión de Django
        # Si tu chatbot está integrado con un frontend, puedes obtener el usuario autenticado
        user = None  # Deberías obtener el usuario autenticado desde Django si es necesario

        if user_input.lower() == "salir":
            print("¡Hasta luego!")
            break
        
        # Obtener la respuesta del chatbot y registrar la interacción
        response = get_chatbot_response(user_input, user)
        print(f"Bot: {response}")
