import joblib

# Cargar el modelo previamente entrenado
model = joblib.load('chatbot_model.pkl')

# Función para predecir la respuesta
def get_response(user_input):
    prediction = model.predict([user_input])
    return prediction[0]


