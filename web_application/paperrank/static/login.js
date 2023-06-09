// Show password
document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('new-password');
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

    // Cambio del botón de acceso al cambio de idioma
    const button = document.getElementById("idioma");
    var languageImg = document.getElementById("config-img");
    var languageText = document.getElementById("language-dropdown");

    button.addEventListener('mouseover', function () {
        languageText.style.color = "#7453c3";
        languageImg.src = '/static/images/lang-hover.png';
    });
    button.addEventListener('mouseout', function () {
        languageText.style.color = "black";
        languageImg.src = '/static/images/lang_bl.png';
    });
});
