document.addEventListener("DOMContentLoaded", function() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const collectionSelect = document.getElementById('collectionSelect');
    const newCollectionInput = document.getElementById('newCollection');
    const uploadForm = document.getElementById('uploadForm');
    const progressBar = document.getElementById('progressBar');
    const progressPercent = document.getElementById('progressPercent');
    const progressBarContainer = document.querySelector('.progress-bar-container');

    // Cargar colecciones en el selector
    function loadCollections() {
        fetch('http://localhost:8000/collections')
            .then(response => response.json())
            .then(data => {
                collectionSelect.innerHTML = '<option value="">-- Select Collection --</option>'; // Limpiar opciones
                data.collections_name.forEach(collectionName => {
                    const option = document.createElement('option');
                    option.value = collectionName;
                    option.textContent = collectionName;
                    collectionSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching collections:', error));
    }

    // Configurar área de arrastre
    dropzone.addEventListener('click', () => fileInput.click());
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragging');
    });
    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragging');
    });
    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragging');
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
        }
    });

    // Manejar envío del formulario
    uploadForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const formData = new FormData();
        for (const file of fileInput.files) {
            formData.append('file', file);
        }

        const collectionName = collectionSelect.value || newCollectionInput.value;
        formData.append('name_collection', collectionName);
        // Usar XMLHttpRequest para monitorear el progreso
        const xhr = new XMLHttpRequest();

        // Mostrar la barra de progreso
        progressBarContainer.style.display = 'block';
        progressPercent.style.display = 'block';
        xhr.upload.addEventListener('progress', function(event) {
            if (event.lengthComputable) {
                const percentComplete = (event.loaded / event.total) * 100;
                progressBar.style.width = percentComplete + "%";
                progressPercent.textContent = Math.round(percentComplete) + "%";
            }
        });

        xhr.onload = function() {
            if (xhr.status === 200) {
                alert('Files uploaded successfully!');
                // Resetear la barra de progreso
                progressBar.style.width = "0%";
                progressPercent.textContent = "0%";
                progressBarContainer.style.display = 'none';
                progressPercent.style.display = 'none';

                // Limpiar el input de archivo y el campo de colección
                fileInput.value = '';
                newCollectionInput.value = '';
            } else {
                alert('Error uploading files.');
            }
        };

        xhr.onerror = function() {
            alert('An error occurred during the upload.');
        };

        // Configurar la solicitud POST
        xhr.open('POST', 'http://localhost:8000/add_document');
        xhr.send(formData);
    });

    //     fetch('http://localhost:8000/add_document', {
    //         method: 'POST',
    //         body: formData
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log('Upload response:', data);
    //         alert('Files uploaded successfully!');
    //         fileInput.value = ''; // Limpiar el input
    //         newCollectionInput.value = ''; // Limpiar el campo de colección nueva
    //     })
    //     .catch(error => console.error('Error uploading files:', error));
    // });

    // Cargar colecciones al inicio
    loadCollections();
});
