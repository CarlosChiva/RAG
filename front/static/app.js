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
        console.log("Collections data:", data);  // Verifica los datos recibidos
        collectionsList.innerHTML = "";  // Limpiar la lista antes de agregar nuevos elementos
        data.collections_name.forEach((collectionName) => {
            const listItem = document.createElement("li");
            listItem.textContent = collectionName;
            listItem.dataset.collectionName = collectionName;  // Usar el nombre de la colección como atributo
            listItem.classList.add("collection-item");
            listItem.addEventListener("click", function() {
                selectCollection(this);
            });
            collectionsList.appendChild(listItem);
        });
    })
    .catch(error => console.error('Error fetching collections:', error));
}

// Función para seleccionar una colección y enviar la solicitud POST
   // Función para seleccionar una colección y enviar la solicitud POST
function selectCollection(element) {
const previouslySelected = document.querySelector(".selected");
if (previouslySelected) {
    previouslySelected.classList.remove("selected");
}
element.classList.add("selected");

selectedCollection = element.dataset.collectionName;  // Usar el nombre de la colección seleccionada
console.log("Selected collection:", selectedCollection);

// Enviar la solicitud POST para cambiar el nombre de la colección
fetch('http://localhost:8000/change-collection-name', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({ collection_name: selectedCollection })
})
.then(response => response.json())
.then(data => {
    console.log("Collection change response:", data);
    // Puedes manejar la respuesta aquí si es necesario
})
.catch(error => console.error('Error changing collection name:', error));
}

// Función para enviar el mensaje
    // Cargar las colecciones al inicio
    loadCollections();

    // Event listener para el botón de enviar
    sendButton.addEventListener("click", function() {
        const message = inputText.value.trim();
        if (!message || !selectedCollection) {
            alert("Please enter a message and select a collection.");
            return;
        }

        // Crear los parámetros para la solicitud GET
        const params = new URLSearchParams({
            input: message,  // Usa 'input' como parámetro de consulta
        });

        // Realizar la solicitud GET con fetch
        fetch(`http://localhost:8000/llm-response?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                console.log("Received data:", data);  // Agrega esta línea
                // Mostrar la respuesta en el área de chat
                const messageElement = document.createElement("div");
                messageElement.textContent = `Bot: ${data}`;  // Asume que la respuesta tiene una propiedad 'answer'
                chatOutput.appendChild(messageElement);
                chatOutput.scrollTop = chatOutput.scrollHeight; // Desplazar al final
                inputText.value = ""; // Limpiar el input
            })
            .catch(error => console.error('Error sending message:', error));

    });
});