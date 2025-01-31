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
  const menuButton = document.getElementById("menuButton");
  if (!token) {
    alert("Token expired. Please, sing up again");
    window.location.href = "index.html";
  }


  let selectedCollection = null;
  toggleButton.addEventListener('click', function() {
    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('expanded');
  });
  logoutButton.addEventListener("click", function() {
    if (confirm("Are you sure you want to logout?")) {
        localStorage.removeItem("access_token");
        window.location.href = "index.html";
    }
  });
  menuButton.addEventListener("click", function() {
    window.location.href = "menu.html";
  });
  // load collections from rag server
  function loadCollections() {
  
    fetch('http://127.0.0.1:8000/collections', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => response.json())
    .then(data => {
 
      collectionsList.innerHTML = ""; 
      if (data.collections_name.length === 0) {
        window.location.href = "upload.html";
      }
      data.collections_name.forEach((collectionName) => {
        const listItem = document.createElement("li");
        const button = document.createElement("button"); 

        listItem.textContent = collectionName;
        listItem.dataset.collectionName = collectionName; 
        listItem.classList.add("collection-item");

        button.textContent = "-"; 
        button.classList.add("delete-button"); 

        listItem.appendChild(button); 
        listItem.addEventListener("click", function() {
          selectCollection(this);
        });
        collectionsList.appendChild(listItem);
  
        button.addEventListener("click", function() {
          deleteCollection(collectionName, this);
        });
      });
    })
    .catch(error => console.error('Error fetching collections:', error));
  }
    
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
      body: JSON.stringify({ collection_name: name }) 
    })
      .then(response => response.json())
      .then(data => console.log("Collection deleted:", data))
      .catch(error => console.error('Error deleting collection:', error));
  
    listItem.remove(); 
  }
  function selectCollection(element) {
    const previouslySelected = document.querySelector(".selected");
    if (previouslySelected) {
      previouslySelected.classList.remove("selected");
    }
    element.classList.add("selected");

    selectedCollection = element.dataset.collectionName; 
    console.log("Selected collection:", selectedCollection);
  }

  loadCollections();

  sendButton.addEventListener("click", function() {
    const message = inputText.value.trim();
    if (!message || !selectedCollection) {
        alert("Please enter a message and select a collection.");
        return;
    }
    sendButton.innerHTML = '<div class="spinner"></div>';
    sendButton.disabled = true;


    const userMessageElement = document.createElement("div");
    userMessageElement.textContent = `${message}`;
    userMessageElement.classList.add("message", "user-message");
    chatOutput.appendChild(userMessageElement);

    chatOutput.scrollTop = chatOutput.scrollHeight;

    inputText.value = "";

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

        const botMessageElement = document.createElement("div");
        botMessageElement.classList.add("message", "bot-message");
        chatOutput.appendChild(botMessageElement);

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

        typeText(botMessageElement, data);  

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