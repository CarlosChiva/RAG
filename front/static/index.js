const loginForm = document.getElementById('loginForm');
const formTitle = document.getElementById('formTitle');
const submitButton = document.getElementById('submitButton');
const signUpLink = document.getElementById('signUpLink');

let isSignUpMode = false; // Estado para determinar si estamos en modo Sign Up o Login

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (token) {
        window.location.href = 'menu.html';
    } else {
        console.log('No JWT found, staying on index.html.');
    }
});

// Manejar el evento del enlace "Sign Up"
// Manejar el evento del enlace "Sign Up"
signUpLink.addEventListener('click', (e) => {
    e.preventDefault();
    isSignUpMode = !isSignUpMode; // Cambiar el estado entre Sign Up y Login

    // Aplicar animación de transición
    loginForm.classList.add('fade-transition');
    setTimeout(() => {
        if (isSignUpMode) {
            // Cambiar a modo Sign Up
            formTitle.textContent = 'Sign Up';
            submitButton.textContent = 'Sign Up';
            submitButton.setAttribute('data-action', 'sign_up');
            signUpLink.textContent = 'Log In';

            loginForm.removeEventListener('submit', handleLoginSubmit);
            loginForm.addEventListener('submit', handleSignUpSubmit);
        } else {
            // Volver a modo Login
            formTitle.textContent = 'Login';
            submitButton.textContent = 'Log In';
            submitButton.setAttribute('data-action', 'log_in');
            signUpLink.textContent = 'Sign Up';

            loginForm.removeEventListener('submit', handleSignUpSubmit);
            loginForm.addEventListener('submit', handleLoginSubmit);
        }

        // Eliminar clase de transición después de aplicar cambios
        loginForm.classList.remove('fade-transition');
    }, 500); // Duración de la animación
});

// Función para manejar el formulario de inicio de sesión
async function handleLoginSubmit(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`http://localhost:8000/log-in?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Login failed.');
        }

        const result = await response.json();
        localStorage.setItem('access_token',"Bearer "+ result.access_token);
        localStorage.setItem('user_name',username);
        alert('Logged in successfully!');
        window.location.href = 'menu.html';
    } catch (error) {
        console.error(error);
        alert(error.message);
    }
}

// Función para manejar el formulario de registro
async function handleSignUpSubmit(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://localhost:8000/sing_up', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Sign-up failed.');
        }

        const result = await response.json();
        localStorage.setItem('access_token', result.access_token);
        alert('User signed up successfully!');
        window.location.href = 'chat.html';
    } catch (error) {
        console.error(error);
        alert(error.message);
    }
}

// Asociar la función de inicio de sesión al evento submit inicialmente
loginForm.addEventListener('submit', handleLoginSubmit);
