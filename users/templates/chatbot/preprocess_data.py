import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import json
import os

# Descargar recursos de NLTK si no los tienes
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Inicializar el lematizador y la lista de stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('spanish'))

def preprocess_text(text):
    """
    Preprocesa un texto:
    1. Tokeniza el texto en palabras.
    2. Elimina las stopwords.
    3. Lematiza las palabras.
    4. Convierte las palabras a minúsculas.
    """
    # Tokenizar el texto (dividir en palabras)
    words = word_tokenize(text)
    
    # Eliminar stopwords y lematizar
    processed_words = [lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in stop_words and word.isalpha()]
    
    # Unir las palabras procesadas de nuevo en una cadena
    return " ".join(processed_words)

def preprocess_data(input_file, output_file):
    """
    Lee un archivo JSON con preguntas y respuestas,
    procesa los textos y guarda el resultado en un archivo de salida.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Preprocesar las preguntas y respuestas
    for item in data:
        item['question'] = preprocess_text(item['question'])
        item['answer'] = preprocess_text(item['answer'])

    # Guardar los datos preprocesados en un archivo de salida
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

    print(f"Datos procesados y guardados en {output_file}")

if __name__ == "__main__":
    # Asegúrate de ajustar las rutas de tus archivos de entrada y salida
    input_file = 'chatbot_data.json'  # Archivo original de datos (preguntas y respuestas)
    output_file = 'chatbot_data_processed.json'  # Archivo con los datos procesados
    
    # Preprocesar los datos
    preprocess_data(input_file, output_file)
