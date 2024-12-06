from shelters.models import Animal  # Asegúrate de importar el modelo correcto

def encontrar_animal_ideal(respuestas, especie):
    puntuaciones = []

    # Filtramos los animales por la especie seleccionada (perro o gato)
    animales = Animal.objects.filter(species=especie, adoption_status='disponible')

    for animal in animales:
        puntuacion = 0

        # Comparar las respuestas del usuario con los atributos del animal
        if respuestas['size'] == animal.size:
            puntuacion += 3
        if respuestas['energy'] == animal.energy:
            puntuacion += 3
        if respuestas['fur'] == animal.fur:
            puntuacion += 2
        if respuestas['personality'] == animal.personality:
            puntuacion += 3

        # Si es un perro, evaluamos los campos adicionales específicos de perros
        if especie == 'perro':
            if respuestas['ejercicio'] == animal.energy:  # Ejercicio y energía se correlacionan para perros
                puntuacion += 3

        # Si es un gato, evaluamos los campos adicionales específicos de gatos
        if especie == 'gato':
            # Para los gatos, podríamos agregar atributos como "actividad", si fuera relevante
            if respuestas.get('actividad', '') == animal.energy:  # Adaptamos energía para gatos
                puntuacion += 3

        puntuaciones.append((animal, puntuacion))

    # Ordenar los animales por la puntuación más alta
    puntuaciones.sort(key=lambda x: x[1], reverse=True)
    # Si encontramos algún animal ideal
    if puntuaciones and puntuaciones[0][1] > 0:  # Asegurarse de que haya alguna puntuación positiva
        animal_ideal = puntuaciones[0][0]
    else:
        animal_ideal = None

    return animal_ideal