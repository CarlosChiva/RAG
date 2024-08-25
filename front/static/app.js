document.addEventListener("DOMContentLoaded", function() {
    const collectionsList = document.getElementById("collections-list");
    const sendButton = document.getElementById("sendButton");
    const inputText = document.getElementById("inputText");
    const chatOutput = document.getElementById("chat-output");

    let selectedCollection = null;

    // Función para cargar las colecciones desde el backend
    function loadCollections() {
        fetch('http://localhost:8000/collections')
            .then(response => response.json())
            .then(data => {
                collectionsList.innerHTML = "";  // Limpiar la lista antes de agregar nuevos elementos
                data.collections_name.forEach((collectionName, index) => {
                    const listItem = document.createElement("li");
                    listItem.textContent = collectionName;
                    listItem.dataset.collectionId = index;  // Usar el índice como ID de la colección
                                        // Crear botón de eliminación
                    const deleteButton = document.createElement("button");
                    deleteButton.textContent = "❌";  // Símbolo de eliminación
                    deleteButton.style.marginLeft = "10px";
                    deleteButton.addEventListener("click", function(event) {
                    event.stopPropagation();  // Evitar que se dispare el evento de selección
                    deleteCollection(index);  // Llamar a la función para eliminar la colección
                });
                    listItem.appendChild(deleteButton);  // Agregar el botón al elemento de la lista

                    listItem.addEventListener("click", function() {
                        selectCollection(this);
                    });
                    collectionsList.appendChild(listItem);
                });
            })
            .catch(error => console.error('Error fetching collections:', error));
    }
    // Función para eliminar una colección
    function deleteCollection(collectionId) {
        fetch(`http://localhost:8000/collections/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: collectionId }),
        })
        .then(response => {
            if (response.ok) {
                loadCollections();  // Refrescar la lista tras la eliminación
            } else {
                console.error('Error deleting collection');
            }
        })
        .catch(error => console.error('Error deleting collection:', error));
    }
    // Función para seleccionar una colección
    function selectCollection(element) {
        const previouslySelected = document.querySelector(".selected");
        if (previouslySelected) {
            previouslySelected.classList.remove("selected");
        }
        element.classList.add("selected");
        selectedCollection = element.dataset.collectionId;
    }

    // Función para enviar el mensaje
    function sendMessage() {
        const message = inputText.value.trim();
        if (!message || !selectedCollection) {
            alert("Please enter a message and select a collection.");
            return;
        }

        fetch(`http://localhost:8000/llm-response?message=${encodeURIComponent(message)}&collection=${selectedCollection}`)
            .then(response => response.json())
            .then(data => {
                // Mostrar la respuesta en el área de chat
                const messageElement = document.createElement("div");
                messageElement.textContent = `Bot: ${data.answer}`;
                chatOutput.appendChild(messageElement);
                chatOutput.scrollTop = chatOutput.scrollHeight; // Desplazar al final
                inputText.value = ""; // Limpiar el input
            })
            .catch(error => console.error('Error sending message:', error));
    }

    // Event listener para el botón de enviar
    sendButton.addEventListener("click", sendMessage);

    // Cargar las colecciones al inicio
    loadCollections();
});
