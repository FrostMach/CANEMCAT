import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle

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
with open('chatbot_data.json', 'r', encoding='utf-8') as f:
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

# Función para obtener la respuesta del chatbot
def get_chatbot_response(user_input):
    # Convertir la frase del usuario en un "bag of words"
    bow_input = bow(user_input, words)
    
    # Predecir la clase (intención) de la frase del usuario
    prediction = model.predict([bow_input])
    predicted_class = prediction[0]
    
    # Buscar la respuesta correspondiente
    response = ""
    for intent in intents['intents']:
        if intent['tag'] == classes[predicted_class]:
            response = np.random.choice(intent['responses'])
            break
    # Si no se encuentra respuesta, devolver mensaje por defecto
    if not response:
        response = "Lo siento, no entiendo esa pregunta. ¿Puedes preguntar de otra manera?"
    
    return response

# Probar el chatbot
if __name__ == "__main__":
    while True:
        # Recibir la entrada del usuario
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            print("¡Hasta luego!")
            break
        
        # Obtener la respuesta del chatbot
        response = get_chatbot_response(user_input)
        print(f"Bot: {response}")

