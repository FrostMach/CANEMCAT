document.addEventListener("DOMContentLoaded", () => {
    const eventModal = new bootstrap.Modal(document.getElementById("eventModal"));
    const eventDateInput = document.getElementById("event-date");
    const eventDescriptionInput = document.getElementById("event-description");
    const startTimeInput = document.getElementById("start-time");
    const endTimeInput = document.getElementById("end-time");
    const eventColorInput = document.getElementById("event-color");
    const saveEventButton = document.getElementById("save-event");
    const editEventButton = document.getElementById("edit-event");

    let currentEditingEvent = null;

    // Cerrar modal
    document.querySelector('.btn-close').addEventListener('click', () => {
        eventModal.hide();
    });

    // Función para cargar la información de un evento en el modal para editarlo
    function openEditModal(event) {
        // Asegúrate de que el evento se pase correctamente y los campos se actualicen
        eventDateInput.value = event.date;
        eventDescriptionInput.value = event.description;
        startTimeInput.value = event.start_time;
        endTimeInput.value = event.end_time;
        eventColorInput.value = event.color;

        // Mostrar el botón de editar solo si estamos editando
        editEventButton.style.display = "inline-block";
        saveEventButton.style.display = "none"; // Ocultar el botón de guardar

        // Guardamos el evento que estamos editando
        currentEditingEvent = event;

        // Abrir el modal para editar el evento
        setTimeout(() => {
            eventModal.show();
        }, 100);
    }

    function openNewEventModal(date) {
        // Asigna la fecha seleccionada
        eventDateInput.value = date;

        // Limpia todos los campos para un nuevo evento
        eventDescriptionInput.value = "";
        startTimeInput.value = "";
        endTimeInput.value = "";
        eventColorInput.value = "#007bff"; // Color predeterminado

        // Restablece el estado de edición
        currentEditingEvent = null;

        // Oculta el botón de editar y muestra el botón de guardar
        editEventButton.style.display = "none";
        saveEventButton.style.display = "inline-block";

        // Asegúrate de que los campos son editables
        eventDateInput.disabled = false;
        eventDescriptionInput.disabled = false;
        startTimeInput.disabled = false;
        endTimeInput.disabled = false;
        eventColorInput.disabled = false;

        // Abre el modal
        eventModal.show();
    }

    saveEventButton.addEventListener('click', () => {
        // Obtén los datos del formulario
        const date = eventDateInput.value;
        const description = eventDescriptionInput.value;
        const startTime = startTimeInput.value;
        const endTime = endTimeInput.value;
        const color = eventColorInput.value;
        console.log(eventDateInput); // ¿Es null?
        console.log(eventDescriptionInput);
        console.log(startTimeInput);
        console.log(endTimeInput);
        console.log(eventColorInput);

        console.log({ date, description, startTime, endTime, color }); // Debug para confirmar valores

        // Valida que los campos no estén vacíos
        if (!description || !startTime || !endTime) {
            alert("Por favor, completa todos los campos del evento.");
            return;
        }

        // Prepara los datos del evento
        const newEvent = {
            date: date,
            description: description,
            start_time: startTime,
            end_time: endTime,
            color: color,
        };

        // Lógica para guardar el evento en el backend
        fetch('/save-event/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify(newEvent),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    alert("Evento creado exitosamente.");
                    eventModal.hide(); // Cierra el modal

                    // Aquí actualiza tu calendario con los nuevos eventos
                    if (!events[date]) {
                        events[date] = [];
                    }
                    events[date].push(data.event);
                    updateCalendar(); // Suponiendo que tienes esta función
                } else {
                    alert("Error al guardar el evento.");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Hubo un error al guardar el evento.");
            });

    });


    // Exponer funciones para que el archivo de calendario.js pueda llamarlas
    window.openNewEventModal = openNewEventModal;
    window.openEditModal = openEditModal;
});
