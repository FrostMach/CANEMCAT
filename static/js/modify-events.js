document.addEventListener("DOMContentLoaded", () => {
    const eventModal = new bootstrap.Modal(document.getElementById("eventModal"));
    const eventDateInput = document.getElementById("event-date");
    const eventDescriptionInput = document.getElementById("event-description");
    const startTimeInput = document.getElementById("start-time");
    const endTimeInput = document.getElementById("end-time");
    const eventColorInput = document.getElementById("event-color");
    const editEventButton = document.getElementById("edit-event");
    console.log(document.getElementById("edit-event"));

    if (editButton) {
        editButton.addEventListener("click", () => {
            console.log("Botón de editar evento presionado");
            console.log(document.getElementById("edit-event"));

            function openEditModal(event) {
                eventDateInput.value = event.date;
                eventDescriptionInput.value = event.description;
                startTimeInput.value = event.start_time;
                endTimeInput.value = event.end_time;
                eventColorInput.value = event.color;

                currentEditingEvent = event;
                eventModal.show();
            }

            // Editar un evento existente
            editEventButton.addEventListener("click", () => {
                const updatedEvent = {
                    id: currentEditingEvent.id,
                    date: eventDateInput.value,
                    description: eventDescriptionInput.value,
                    start_time: startTimeInput.value,
                    end_time: endTimeInput.value,
                    color: eventColorInput.value,
                };

                fetch(`/update-event/${updatedEvent.id}/`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                    },
                    body: JSON.stringify(updatedEvent),
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert("Evento actualizado correctamente.");
                            eventModal.hide();
                            location.reload(); // Recarga la página para reflejar cambios
                        } else {
                            alert("Error al actualizar el evento.");
                        }
                    })
                    .catch(error => {
                        console.error("Error al actualizar el evento:", error);
                        alert("Hubo un error al actualizar el evento.");
                    });
            });
        });
    } else {
        console.error("Elemento 'edit-event' no encontrado en el DOM.");
    }
const deleteEventButton = document.getElementById("delete-event");

let currentEditingEvent = null;

// Abre el modal para editar un evento


// Borrar un evento
deleteEventButton.addEventListener("click", () => {
    fetch(`/delete-event/${currentEditingEvent.id}/`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Evento eliminado correctamente.");
                eventModal.hide();
                location.reload(); // Recarga la página para reflejar cambios
            } else {
                alert("Error al eliminar el evento.");
            }
        })
        .catch(error => {
            console.error("Error al eliminar el evento:", error);
            alert("Hubo un error al eliminar el evento.");
        });
});

// Exponer funciones globalmente
window.openEditModal = openEditModal;
});
