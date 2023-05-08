// Validate fields 
function validateForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // TO DO: comprobar usuario y email -> backend

    if (username != "usuario" || password != "Hola1111") {
        alert("Usuario o contraseña incorrectos");
        return false;
    } else {
        // TO DO: pasar información de inicio de sesión:
        // Se puede enviar información de usuario a la página principal usando query string, cookies, localStorage, etc.
        window.location.href = "index.html";
        return false;
    }
}


// Show password
document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password');
    const showPasswordButton = document.getElementById('show-password');

    showPasswordButton.addEventListener('click', function () {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            showPasswordButton.src = "/static/images/ojo.png";
            showPasswordButton.alt = 'Ocultar contraseña';
        } else {
            passwordInput.type = 'password';
            showPasswordButton.src = "/static/images/ojotachado.png";
            showPasswordButton.alt = 'Mostrar contraseña';
        }
    });
});		
