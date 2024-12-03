import json
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
from sklearn.preprocessing import LabelEncoder
from ignore_words import ignore_words  # Importa la lista de palabras a ignorar

# Descargar recursos necesarios de nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)  # Tokenizamos la oración
    sentence_words = [lemmatizer.lemmatize(w.lower()) for w in sentence_words if w.lower() not in ignore_words]
    return sentence_words
# Inicializar el lematizador
lemmatizer = WordNetLemmatizer()

def preprocess_data(data):
    # Inicializar listas para las palabras, las clases (intenciones) y los patrones de entrenamiento
    words = []
    classes = []
    documents = []

    # Recorremos los datos de entrenamiento
    for intent in data['intents']:
        for pattern in intent['patterns']:
            # Tokenizamos las palabras
            word_list = nltk.word_tokenize(pattern)
            words.extend(word_list)
            documents.append((pattern, intent['intent']))
        
        # Añadimos la intención a la lista de clases
        classes.append(intent['intent'])

    # Lematizamos las palabras y las convertimos a minúsculas, eliminamos duplicados
    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
    words = sorted(list(set(words)))

    # Eliminamos las duplicadas de las clases (intenciones)
    classes = sorted(list(set(classes)))

    # Preparamos los datos de entrenamiento: cada patrón se convierte en una lista de 0's y 1's
    training_sentences = []
    training_labels = []

    # Recorremos los documentos y creamos las frases y las etiquetas correspondientes
    for doc in documents:
        sentence = doc[0]
        intent = doc[1]
        
        # Crear una lista de palabras lematizadas para cada patrón
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(w.lower()) for w in sentence_words]
        
        # Usamos un conjunto de palabras de entrenamiento como una representación binaria
        bag = [1 if w in sentence_words else 0 for w in words]
        
        # Añadimos el bag de palabras y la etiqueta correspondiente
        training_sentences.append(bag)
        training_labels.append(classes.index(intent))

    # Convertimos las listas de entrenamiento a arrays de NumPy
    training_sentences = np.array(training_sentences)
    training_labels = np.array(training_labels)

    return training_sentences, training_labels, words, classes

# Cargar los datos del archivo JSON
with open('chatbot_data.json') as f:
    data = json.load(f)

# Preprocesar los datos
training_sentences, training_labels, words, classes = preprocess_data(data)

import os

# Archivos de destino
files = ['training_sentences.npy', 'training_labels.npy', 'words.npy', 'classes.npy']

# Eliminar archivos si existen
for file in files:
    if os.path.exists(file):
        os.remove(file)

# Guardar los datos preprocesados
np.save('training_sentences.npy', training_sentences)
np.save('training_labels.npy', training_labels)
np.save('words.npy', words)
np.save('classes.npy', classes)

