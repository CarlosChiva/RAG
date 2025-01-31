document.addEventListener("DOMContentLoaded", async function() {
    const token = localStorage.getItem('access_token');
    const username = localStorage.getItem('user_name');
    const logoutButton = document.getElementById('logoutButton');
    const iconContainer = document.getElementById("iconContainer");
    const sidebarIcons = document.getElementById("sidebarIcons");
    document.getElementById('Tittle').textContent = "Welcome " + username;

    const icons = {
        "pdf": "/images/pdf.png",
        "excel": "/images/excel.png",
        "multimedia": "/images/multimedia.png",
        "audio": "/images/chatbot.png"
    };
    
    if (!token) {
        alert('Token expired. Please, sing up again');
        window.location.href = 'index.html';
    }
    
    
    logoutButton.addEventListener('click', function() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_name');
        window.location.href = 'index.html';
    });


    // get services user by user
    async function fetchServices() {
        try {
            const response = await fetch("http://localhost:8001/get-services", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Error al obtener servicios");
            }

            const services = await response.json();
            updateIcons(services.services);
        } catch (error) {
            console.error("Error al obtener servicios activos:", error);
        }
    }

    // get list of available services don't use by user
    async function fetchAvailableServices() {
        try {
            const response = await fetch("http://localhost:8001/get-services-available", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Error al obtener servicios disponibles");
            }

            const services = await response.json();
           await updateSidebar(services.services);
        } catch (error) {
            console.error("Error al obtener servicios disponibles:", error);
        }
    }

    // load icons with services used by user in window
    function updateIcons(services) {
        iconContainer.innerHTML = `
            <a href="chat.html" class="icon-button">
                <img src="/images/chatbot.png" alt="Chat">
            </a>
        `;

        services.forEach(service => {
            if (icons[service]) {
                const newButton = document.createElement("a");
                newButton.href = `/${service}.html`;
                newButton.classList.add("icon-button");

                const newImg = document.createElement("img");
                newImg.src = icons[service];
                newImg.alt = service;

                newButton.appendChild(newImg);
                iconContainer.appendChild(newButton);
            }
        });
    }

    // load sidebar with services available don't use by user yet
    async function updateSidebar(services) {
        sidebarIcons.innerHTML = ""; // Limpiar contenido previo

        services.forEach(service => {
            if (icons[service]) {
                const serviceButton = document.createElement("a");
                serviceButton.href = "#";
                serviceButton.classList.add("icon-sidebar-button");

                const serviceImg = document.createElement("img");
                serviceImg.src = icons[service];
                serviceImg.alt = service;

                serviceButton.appendChild(serviceImg);
                sidebarIcons.appendChild(serviceButton);

                // listener to add service to services used by user
                serviceButton.addEventListener("click", async function() {
                    await select_service(service);
                });
            }
        });
    }

    // Record service selected by user such as used
    async function select_service(service) {
        try {
            const response = await fetch(`http://localhost:8001/add-services?service=${encodeURIComponent(service)}`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Error al obtener servicios disponibles");
            }
            window.location.href = `/${service}.html`;

        } catch (error) {
            console.error("Error al obtener servicios disponibles:", error);
        }

    };

    // listener to open sidebar
    document.getElementById("openSidebar").addEventListener("click", function() {
        document.getElementById("sidebar").classList.add("active");
    });
    // listener to close sidebar
    document.getElementById("closeSidebar").addEventListener("click", function() {
        document.getElementById("sidebar").classList.remove("active");
    });


    // Load all services to load window 
    fetchServices();
    fetchAvailableServices();
});
