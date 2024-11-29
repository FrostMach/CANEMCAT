import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Descargar recursos de NLTK si no los tienes
nltk.download('punkt')

# Cargar los datos preprocesados (del archivo JSON)
with open('chatbot_data_processed.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extraer las preguntas y respuestas
questions = [item['question'] for item in data]
answers = [item['answer'] for item in data]

# Dividir los datos en entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(questions, answers, test_size=0.2, random_state=42)

# Crear un pipeline con TfidfVectorizer y el clasificador Naive Bayes
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Entrenar el modelo
model.fit(X_train, y_train)

# Realizar predicciones sobre el conjunto de prueba
predictions = model.predict(X_test)

# Evaluar el rendimiento del modelo
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Guardar el modelo entrenado para usarlo en el chatbot
joblib.dump(model, 'chatbot_model.pkl')

print("Modelo entrenado y guardado como 'chatbot_model.pkl'")
