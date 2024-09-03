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
        console.log("Collections data:", data); // Verifica los datos recibidos
        collectionsList.innerHTML = ""; // Limpiar la lista antes de agregar nuevos elementos
        data.collections_name.forEach((collectionName) => {
          const listItem = document.createElement("li");
          const button = document.createElement("button"); // Agregar botón para eliminar elemento
  
          listItem.textContent = collectionName;
          listItem.dataset.collectionName = collectionName; // Usar el nombre de la colección como atributo
          listItem.classList.add("collection-item");
  
          button.textContent = "Eliminar"; // Texto del botón
          button.classList.add("delete-button"); // Clase para estilizar el botón
  
          listItem.appendChild(button); // Agregar botón a la lista
          listItem.addEventListener("click", function() {
            selectCollection(this);
          });
          collectionsList.appendChild(listItem);
  
          // Event listener para el botón de eliminación
          button.addEventListener("click", function() {
            deleteCollection(collectionName, this);
          });
        });
      })
      .catch(error => console.error('Error fetching collections:', error));
  }
  
  // Función para eliminar una colección y enviar la solicitud POST
  function deleteCollection(name, element) {
    const previouslySelected = document.querySelector(".selected");
    if (previouslySelected && previouslySelected.dataset.collectionName === name) {
      selectedCollection = null;
      previouslySelected.classList.remove("selected");
    }
    const listItem = element.parentElement;
  
    fetch('http://localhost:8000/delete-collection', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: new URLSearchParams({ collection_name: selectedCollection })
    })
      .then(response => response.json())
      .then(data => console.log("Collection deleted:", data))
      .catch(error => console.error('Error deleting collection:', error));
  
    listItem.remove(); // Eliminar el elemento de la lista
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

        const userMessageElement = document.createElement("div");
        userMessageElement.textContent = `${message}`;
        userMessageElement.classList.add("message", "user-message");
        chatOutput.appendChild(userMessageElement);

        // Desplazar al final del área de chat
        chatOutput.scrollTop = chatOutput.scrollHeight;

        // Limpiar el input
        inputText.value = "";

        // Crear los parámetros para la solicitud GET
        const params = new URLSearchParams({
            input: message,
        });

        // Realizar la solicitud GET con fetch
        fetch(`http://localhost:8000/llm-response?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                console.log("Received data:", data);

                // Crear el elemento del mensaje del bot
                const botMessageElement = document.createElement("div");
                botMessageElement.textContent = `${data}`;  // Asegúrate de que 'data.answer' es la estructura correcta
                botMessageElement.classList.add("message", "bot-message");
                chatOutput.appendChild(botMessageElement);

                // Desplazar al final del área de chat
                chatOutput.scrollTop = chatOutput.scrollHeight;
            })
            .catch(error => console.error('Error sending message:', error));
    });
});