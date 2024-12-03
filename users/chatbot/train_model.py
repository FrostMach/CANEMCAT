import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle

# Cargar los datos preprocesados
training_sentences = np.load('training_sentences.npy')
training_labels = np.load('training_labels.npy')

# Entrenar el modelo con un clasificador simple (Logistic Regression)
model = LogisticRegression(max_iter=200)
model.fit(training_sentences, training_labels)

# Guardar el modelo entrenado
with open('chatbot_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

print("Modelo entrenado y guardado exitosamente.")
