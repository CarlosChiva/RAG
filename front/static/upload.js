document.addEventListener("DOMContentLoaded", function () {
    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("fileInput");
    const collectionSelect = document.getElementById("collectionSelect");
    const newCollectionInput = document.getElementById("newCollection");
    const uploadForm = document.getElementById("uploadForm");
    const loaderContainer = document.querySelector(".loader-container");
    const token = localStorage.getItem("access_token");

        // Función para habilitar/deshabilitar el botón
    function toggleButtonState(isDisabled) {
            uploadButton.disabled = isDisabled;
            uploadButton.style.backgroundColor = isDisabled ? "#666" : "#007bff";
            uploadButton.style.cursor = isDisabled ? "not-allowed" : "pointer";
        }
    // Cargar colecciones al inicio
    async function loadCollections() {
        if (!token) {
            console.error("No token found in localStorage.");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/collections", {
                headers: { Authorization: `Bearer ${token}` },
            });
            const data = await response.json();
            collectionSelect.innerHTML = '<option value="">-- Select Collection --</option>';
            data.collections_name.forEach((name) => {
                const option = document.createElement("option");
                option.value = name;
                option.textContent = name;
                collectionSelect.appendChild(option);
            });
        } catch (error) {
            console.error("Error fetching collections:", error);
        }
    }

    dropzone.addEventListener("click", () => fileInput.click());

    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        if (!fileInput.files.length) {
            alert("Please select a file.");
            return;
        }

        const formData = new FormData();
        for (const file of fileInput.files) {
            formData.append("file", file);
        }
        formData.append(
            "name_collection",
            collectionSelect.value || newCollectionInput.value
        );

        try {
            toggleButtonState(true); // Deshabilitar botón

            loaderContainer.style.display = "block"; // Mostrar círculo de carga

            const response = await fetch("http://localhost:8000/add_document", {
                method: "POST",
                headers: { Authorization: `Bearer ${token}` },
                body: formData,
            });

            const data = await response.json();
            if (response.ok) {
                alert("Files uploaded successfully!");
            } else {
                alert(data.error || "Error uploading files.");
            }
        } catch (error) {
            alert("An error occurred during the upload.");
        } finally {
            loaderContainer.style.display = "none"; // Ocultar círculo de carga
            toggleButtonState(false); // Habilitar botón

        }
    });

    loadCollections();
});
