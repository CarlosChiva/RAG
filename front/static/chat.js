document.addEventListener("DOMContentLoaded", function() {
  const sidebar = document.getElementById('sidebar');
  const toggleButton = document.getElementById('toggleSidebar');
  const mainContent = document.getElementById('.main-content');
  const collectionsList = document.getElementById("collections-list");
  const sendButton = document.getElementById("sendButton");
  const inputText = document.getElementById("inputText");
  const chatOutput = document.getElementById("chat-output");
  const token = localStorage.getItem("access_token");
  const logoutButton = document.getElementById("logoutButton");
  const container = document.getElementById("container");


  let selectedCollection = null;
  toggleButton.addEventListener('click', function() {
    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('expanded');
});
logoutButton.addEventListener("click", function() {
  if (confirm("Are you sure you want to logout?")) {
      // Limpia el token del localStorage
      localStorage.removeItem("access_token");
      // Redirige a la página de inicio de sesión
      window.location.href = "index.html";
  }
});
  // Función para cargar las colecciones desde el backend
  function loadCollections() {
    if (!token) {
      console.error("No token found in localStorage.");
      return;
    }
  
    fetch('http://127.0.0.1:8000/collections', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
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
    
            button.textContent = "-"; // Texto del botón
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
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`

        },
        body: JSON.stringify({ collection_name: name }) // Enviar el nombre de la colección como JSON
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
          // Cambiar el botón a spinner
          sendButton.innerHTML = '<div class="spinner"></div>';
          sendButton.disabled = true;


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
              collection_name: selectedCollection
          });

          // Realizar la solicitud GET con fetch
          fetch(`http://localhost:8000/llm-response?${params.toString()}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}` // Agregar el JWT al encabezado
            }
        })
              .then(response => response.json())
              .then(data => {
                  console.log("Received data:", data);

                  // Crear el elemento del mensaje del bot
                  const botMessageElement = document.createElement("div");
                  //botMessageElement.textContent = `${data}`;  // Asegúrate de que 'data.answer' es la estructura correcta
                  botMessageElement.classList.add("message", "bot-message");
                  chatOutput.appendChild(botMessageElement);
              // Función para simular la escritura progresiva
                  function typeText(element, text, speed = 20) {
                    let index = 0;
                    function addNextChar() {
                        if (index < text.length) {
                            element.textContent += text.charAt(index);
                            index++;
                            setTimeout(addNextChar, speed);
                        }
                    }
                    addNextChar();
                }

                // Simular la escritura del mensaje
                typeText(botMessageElement, data);  // Asegúrate de que 'data' es el texto correcto.

                  // Desplazar al final del área de chat
                chatOutput.scrollTop = chatOutput.scrollHeight;
              })
              .catch(error => console.error('Error sending message:', error)).finally(() => {
                // Restaurar el botón a su estado original
                sendButton.innerHTML = 'Send';
                sendButton.disabled = false;
            });
            inputText.addEventListener("keypress", function(event) {
              console.log(`Key pressed: ${event.key}`);

              if (event.key === "Enter") {
                sendMessage();
              }
            });
        });

});