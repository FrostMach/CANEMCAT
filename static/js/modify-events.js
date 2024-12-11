document.addEventListener("DOMContentLoaded", () => {
    const eventModal = new bootstrap.Modal(document.getElementById("eventModal"));
    const eventDateInput = document.getElementById("event-date");
    const eventDescriptionInput = document.getElementById("event-description");
    const startTimeInput = document.getElementById("start-time");
    const endTimeInput = document.getElementById("end-time");
    const eventColorInput = document.getElementById("event-color");
    const saveEventButton = document.getElementById("save-event");
    const editEventButton = document.getElementById("edit-event");

    let currentEditingEvent = null;  // Esto debería estar al principio de tu archivo JS

    // Luego, dentro de openEditModal, se actualiza con el evento que estamos editando
    currentEditingEvent = event;
    
    // Función para guardar o editar un evento
    saveEventButton.addEventListener("click", () => {
        const date = eventDateInput.value;
        const description = eventDescriptionInput.value;
        const startTime = startTimeInput.value;
        const endTime = endTimeInput.value;
        const color = eventColorInput.value;

        if (!description || !startTime || !endTime) {
            alert("Por favor, complete todos los campos del evento.");
            return;
        }

        const eventData = {
            date: date,
            description: description,
            start_time: startTime,
            end_time: endTime,
            color: color
        };

        let url = '/save-event/';
        let method = 'POST';

        if (currentEditingEvent) {
            url = `/edit-event/${currentEditingEvent.id}/`; // URL para editar el evento
            method = 'POST'; // Usamos POST para editar
            eventData.id = currentEditingEvent.id; // Incluir el ID del evento que se está editando
        }

        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify(eventData)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Actualizar la lista de eventos en el calendario
                    if (!events[data.event.date]) {
                        events[data.event.date] = [];
                    }

                    const existingEventIndex = events[data.event.date].findIndex(e => e.id === data.event.id);
                    if (existingEventIndex === -1) {
                        events[data.event.date].push(data.event);
                    }

                    // Si estamos editando, actualizamos los detalles del evento en el objeto `events`
                    if (currentEditingEvent) {
                        currentEditingEvent.description = data.event.description;
                        currentEditingEvent.start_time = data.event.start_time;
                        currentEditingEvent.end_time = data.event.end_time;
                        currentEditingEvent.color = data.event.color;
                    }

                    eventModal.hide(); // Cerrar el modal
                    updateCalendar(); // Actualizar el calendario con los cambios
                } else {
                    alert("Hubo un error al guardar el evento.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Hubo un error al guardar el evento.");
            });
    });


    // Editar un evento (esto se activa cuando se hace click sobre un evento en el calendario)
    editEventButton.addEventListener("click", () => {
        // Similar al botón de guardar, pero en lugar de crear uno nuevo, editamos uno existente
        saveEventButton.click();
    });

    // Función para cargar la información de un evento en el modal para editarlo
    function openEditModal(event) {
        console.log("Evento para editar:", event);
    
        // Asignar los valores al modal
        eventDateInput.value = event.date;
        eventDescriptionInput.value = event.description;
        startTimeInput.value = event.start_time;
        endTimeInput.value = event.end_time;
        eventColorInput.value = event.color;
    
        // Almacenamos el evento para futuras modificaciones
        currentEditingEvent = event;
    
        // Usamos setTimeout para asegurar que los valores se asignen antes de abrir el modal
        setTimeout(() => {
            eventModal.show();
        }, 100);
    }
    
    
    

    // Función para abrir el modal y crear un nuevo evento
    function openNewEventModal(date) {
        eventDateInput.value = date;
        eventDescriptionInput.value = "";
        startTimeInput.value = "";
        endTimeInput.value = "";
        endTimeInput.value = "";
        eventColorInput.value = "#007bff"; // Color predeterminado
        currentEditingEvent = null;

        eventModal.show();
    }

    // Exponer funciones para que el archivo de calendario.js pueda llamarlas
    window.openEditModal = openEditModal;
    window.openNewEventModal = openNewEventModal;
});
