from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
import tensorflow as tf
import pickle
import json
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from tensorflow.keras.models import load_model # type: ignore
import os

# Ruta relativa del proyecto (usando __file__ para obtener la ubicación del archivo actual)
project_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene la ruta del archivo Python actual

# Construcción de las rutas para los archivos
tokenizer_path = os.path.join(project_dir, 'models', 'tokenizer.pickle')
label_encoder_path = os.path.join(project_dir, 'models', 'label_encoder.pickle')
model_path = os.path.join(project_dir, 'models', 'chat_model.keras')
chatbot_data_path = os.path.join(project_dir, 'models', 'chatbot_data.json')

# Verificar si el archivo del modelo existe antes de cargarlo
if os.path.exists(model_path):
    model = load_model(model_path)
    print("Modelo cargado con éxito.")
else:
    print("El archivo de modelo no se encuentra en la ruta especificada.")

# Cargar el tokenizer y el label encoder
with open(tokenizer_path, 'rb') as handle:
    tokenizer = pickle.load(handle)

with open(label_encoder_path, 'rb') as handle:
    lbl_encoder = pickle.load(handle)

# Cargar los datos del chatbot (intents y respuestas)
try:
    with open(chatbot_data_path, 'r') as file:
        chatbot_data = json.load(file)
        print("Datos cargados correctamente.")
except FileNotFoundError:
    print(f"El archivo no se encuentra en la ruta: {chatbot_data_path}")
max_len = 25  # Usar el mismo valor que en el entrenamiento

# Vista para interactuar con el chatbot
def chatbot_view(request):
    if model is None:
        return JsonResponse({'response': "El chatbot no está disponible en este momento. Inténtalo más tarde."})
    if request.method == "POST":
        user_input = request.POST.get("message")  # Obtener el mensaje del usuario desde el formulario
        
        if user_input:
            # Preprocesar el mensaje del usuario
            input_seq = tokenizer.texts_to_sequences([user_input])
            padded_input = pad_sequences(input_seq, truncating='post', maxlen=max_len)
            
            # Predecir la respuesta del modelo
            result = model.predict(padded_input)
            tag = lbl_encoder.inverse_transform([np.argmax(result)])  # Obtener la etiqueta predecida
            
            # Obtener la respuesta basada en la etiqueta
            response = None
            for intent in chatbot_data['intents']:  # Aquí accedes a los datos del JSON
                if intent['tag'] == tag[0]:
                    response = np.random.choice(intent['responses'])
                    break
             # Si no se encuentra ninguna respuesta, devolver una respuesta predeterminada
            if not response:
                response = "Lo siento, no entiendo esa pregunta."
                
            return JsonResponse({'response': response})
        
    return render(request, 'chatbot/chat.html')
