const signUpForm = document.getElementById('loginForm');
//const errorDiv = document.getElementById('error');
const formTitle = document.getElementById('formTitle');

document.addEventListener('DOMContentLoaded', () => {
    // Verificar si hay un token JWT en localStorage
    const token = localStorage.getItem('access_token');

    if (token) {
        // Redirigir al chat si existe un token
        window.location.href = 'chat.html';
    } else {
        console.log('No JWT found, staying on index.html.');
    }
});
// Manejar el envío del formulario de registro
signUpForm.addEventListener('submit', async (e) => {
    e.preventDefault();
//    errorDiv.textContent = '';

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        // Hacer la petición al backend
        const response = await fetch('http://localhost:8000/sing_in', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Registration failed.');
        }

        // Parsear la respuesta
        const result = await response.json();

        // Almacenar el token en localStorage
        localStorage.setItem('access_token', result.access_token);

        // Notificar éxito y redirigir
        alert('User registered successfully!');
        window.location.href = 'chat.html'; // Redirigir a la ventana principal
    } catch (error) {
       console.error(error);
        // errorDiv.textContent = error.message;
    }
});