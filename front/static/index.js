const loginForm = document.getElementById('loginForm');
const errorDiv = document.getElementById('error');
const formTitle = document.getElementById('formTitle');

// Handle login form submission
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorDiv.textContent = '';

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`http://localhost:8000/log-in?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`);

        if (!response.ok) {
            throw new Error('Login failed. Check your credentials.');
        }

        const result = await response.json();

        // Redirigir si el login es exitoso
        window.location.href = 'chat.html';
    } catch (error) {
        errorDiv.textContent = error.message;
    }
});

