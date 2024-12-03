import json
import sys
import os

# Establecer el entorno de Django para que funcione el import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))  # Agregar la carpeta del proyecto a sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'CANEMCAT.settings'

import django
django.setup()
from users.models import Intent  # Reemplaza `myapp` con el nombre de tu aplicación.

# Ruta del archivo JSON
json_file_path = 'chatbot_data.json'

# Lee el archivo JSON
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Imprime la estructura de los datos cargados para verificarla
print("Estructura del archivo JSON cargado:", data)

# Accede a la lista de "intents"
if 'intents' in data:
    intents_data = data['intents']
    print(f"Se encontraron {len(intents_data)} intents.")
    
    # Recorre los datos y guarda cada intent en la base de datos
    for item in intents_data:
        print(f"Procesando intent: {item}")  # Imprime el 'item' para revisar su estructura
        
        if isinstance(item, dict):  # Verifica que item es un diccionario
            intent = Intent(
                name=item.get('intent', ''),
                patterns=item.get('patterns', []),
                responses=item.get('responses', [])
            )
            intent.save()
        else:
            print(f"Elemento no es un diccionario: {item}")
else:
    print("No se encontró la clave 'intents' en los datos cargados.")

print("Todos los intents han sido importados.")
