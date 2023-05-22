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
