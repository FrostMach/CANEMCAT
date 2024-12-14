from django.shortcuts import render
from django.http import JsonResponse
import os
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import json

# Inicializar el lematizador
lemmatizer = WordNetLemmatizer()

# Ruta del proyecto
project_dir = os.path.dirname(os.path.abspath(__file__))

# Rutas de los modelos y datos
words_path = os.path.join(project_dir, 'models', 'words.npy')
classes_path = os.path.join(project_dir, 'models', 'classes.npy')
model_path = os.path.join(project_dir, 'models', 'chatbot_model.pkl')
intents_path = os.path.join(project_dir, 'models', 'chatbot_data.json')

# Cargar los datos preprocesados y el modelo
if os.path.exists(words_path) and os.path.exists(classes_path) and os.path.exists(model_path) and os.path.exists(intents_path):
    with open(words_path, 'rb') as f:
        words = np.load(f)

    with open(classes_path, 'rb') as f:
        classes = np.load(f)

    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)

    with open(intents_path, 'r', encoding='utf-8') as f:
        intents = json.load(f)
else:
    raise FileNotFoundError("Uno o más archivos necesarios no se encontraron en las rutas especificadas.")

# Función para procesar la entrada del usuario
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(w.lower()) for w in sentence_words]
    return sentence_words

# Función para crear el "bag of words"
def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [1 if w in sentence_words else 0 for w in words]
    return np.array(bag)

# Vista para interactuar con el chatbot
def chatbot_view(request):
    if request.method == "POST":
        user_input = request.POST.get("message", "").strip()
        if not user_input:
            return JsonResponse({'response': "Por favor, escribe algo para poder responder."})
        
        try:
            # Convertir la entrada del usuario a un "bag of words"
            bow_input = bow(user_input, words)
            
            # Predecir la clase/intención
            prediction = model.predict([bow_input])
            predicted_class = prediction[0]

            # Buscar la respuesta correspondiente en las intenciones
            response = None
            for intent in intents['intents']:
                if intent['tag'] == classes[predicted_class]:
                    response = np.random.choice(intent['responses'])
                    break
            
            if not response:
                response = "Lo siento, no entiendo esa pregunta."
            
            return JsonResponse({'response': response})
        
        except Exception as e:
            return JsonResponse({'response': f"Se produjo un error: {str(e)}"})

    return render(request, 'chatbot/chat.html')
