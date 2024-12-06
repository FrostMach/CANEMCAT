
def calcular_compatibilidad_perro(respuestas):
    puntuacion = 0

    # Lógica de compatibilidad para perros basada en las respuestas
    if respuestas['tamaño'] == 'Mediano':
        puntuacion += 2
    elif respuestas['tamaño'] == 'Grande':
        puntuacion += 1

    if respuestas['edad'] == 'Cachorro':
        puntuacion += 1
    elif respuestas['edad'] == 'Joven':
        puntuacion += 2
    elif respuestas['edad'] == 'Adulto':
        puntuacion += 3
    elif respuestas['edad'] == 'Senior':
        puntuacion += 2

    if respuestas['energia'] == 'Alta':
        puntuacion += 3
    elif respuestas['energia'] == 'Moderada':
        puntuacion += 2
    elif respuestas['energia'] == 'Baja':
        puntuacion += 1

    if respuestas['pelaje'] == 'Pelo largo':
        puntuacion += 1
    elif respuestas['pelaje'] == 'Pelo corto':
        puntuacion += 2

    if respuestas['temperamento'] == 'Activo':
        puntuacion += 3
    elif respuestas['temperamento'] == 'Tranquilo':
        puntuacion += 1

    if respuestas['ejercicio'] == 'Alto':
        puntuacion += 3
    elif respuestas['ejercicio'] == 'Moderado':
        puntuacion += 2
    elif respuestas['ejercicio'] == 'Poco':
        puntuacion += 1

    if respuestas['espacio'] == 'Grande':
        puntuacion += 3
    elif respuestas['espacio'] == 'Mediano':
        puntuacion += 2
    elif respuestas['espacio'] == 'Pequeño':
        puntuacion += 1

    if respuestas['niños'] == 'Sí':
        puntuacion += 3
    elif respuestas['niños'] == 'No':
        puntuacion += 1

    if respuestas['otros_perros'] == 'Sí':
        puntuacion += 3
    elif respuestas['otros_perros'] == 'No':
        puntuacion += 1

    if respuestas['compañía'] == 'Alta':
        puntuacion += 3
    elif respuestas['compañía'] == 'Moderada':
        puntuacion += 2
    elif respuestas['compañía'] == 'Baja':
        puntuacion += 1

    return puntuacion


def calcular_compatibilidad_gato(respuestas):
    puntuacion = 0

    # Lógica de compatibilidad para gatos basada en las respuestas
    if respuestas['tamaño'] == 'Mediano':
        puntuacion += 2
    elif respuestas['tamaño'] == 'Grande':
        puntuacion += 1

    if respuestas['edad'] == 'Cachorro':
        puntuacion += 1
    elif respuestas['edad'] == 'Joven':
        puntuacion += 2
    elif respuestas['edad'] == 'Adulto':
        puntuacion += 3
    elif respuestas['edad'] == 'Senior':
        puntuacion += 2

    if respuestas['actividad'] == 'Alta':
        puntuacion += 3
    elif respuestas['actividad'] == 'Moderada':
        puntuacion += 2
    elif respuestas['actividad'] == 'Baja':
        puntuacion += 1

    if respuestas['pelaje'] == 'Largo':
        puntuacion += 1
    elif respuestas['pelaje'] == 'Corto':
        puntuacion += 2

    if respuestas['personalidad'] == 'Cariñoso':
        puntuacion += 3
    elif respuestas['personalidad'] == 'Juguetón':
        puntuacion += 2
    elif respuestas['personalidad'] == 'Independiente':
        puntuacion += 1

    if respuestas['espacio'] == 'Grande':
        puntuacion += 3
    elif respuestas['espacio'] == 'Mediano':
        puntuacion += 2
    elif respuestas['espacio'] == 'Pequeño':
        puntuacion += 1

    if respuestas['niños'] == 'Sí':
        puntuacion += 3
    elif respuestas['niños'] == 'No':
        puntuacion += 1

    if respuestas['otros_gatos'] == 'Sí':
        puntuacion += 3
    elif respuestas['otros_gatos'] == 'No':
        puntuacion += 1

    if respuestas['compañía'] == 'Alta':
        puntuacion += 3
    elif respuestas['compañía'] == 'Moderada':
        puntuacion += 2
    elif respuestas['compañía'] == 'Baja':
        puntuacion += 1

    return puntuacion

def encontrar_animal_ideal(respuestas, especie):
    puntuaciones = []

    # Filtramos los animales por la especie seleccionada (perro o gato)
    animales = 'shelters.Animal'.objects.filter(species=especie, adoption_status='disponible')

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

    # Retornar el animal con la mayor puntuación
    return puntuaciones[0][0]  # Solo devolvemos el objeto Animal
