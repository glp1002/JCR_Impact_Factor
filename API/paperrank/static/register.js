// Mostrar contraseñas
const passwordInputs = document.querySelectorAll('#new-password');

document.addEventListener('DOMContentLoaded', function () {
    const showPasswordButtons = document.querySelectorAll('#show-password');

    showPasswordButtons.forEach(function (button, index) {
        button.addEventListener('click', function () {
            const passwordInput = passwordInputs[index];
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                button.src = "/static/images/ojo.png";
                button.alt = 'Ocultar contraseña';
            } else {
                passwordInput.type = 'password';
                button.src = "/static/images/ojotachado.png";
                button.alt = 'Mostrar contraseña';
            }
        });
    });
});


// Comprobar contraseña
const passwordInput = document.getElementById('new-password');
const passwordRequirements = document.getElementById('password-requirements');

passwordInput.addEventListener('input', function () {
    const password = passwordInput.value;

    // Verificar los requisitos mínimos de la contraseña
    let requirements = [];
    if (password.length < 8) {
        requirements.push('al menos 8 caracteres');
    }
    if (!/\d/.test(password)) {
        requirements.push('al menos un número');
    }
    if (!/[A-Z]/.test(password)) {
        requirements.push('al menos una letra mayúscula');
    }

    // Mostrar los requisitos si la contraseña no cumple con ellos
    if (requirements.length > 0) {
        passwordRequirements.innerText = 'La contraseña debe contener: ' + requirements.join(', ');
    } else {
        passwordRequirements.innerText = '';
    }
});

// Comprobar correo
const emailInput = document.getElementById('new-email');
const emailRequirements = document.getElementById('email-requirements');

emailInput.addEventListener('input', function () {
    const email = emailInput.value;

    // Verificar los requisitos mínimos del correo electrónico
    let requirements = [];
    if (!/^\S+@\S+\.\S+$/.test(email)) {
        requirements.push('una dirección válida');
    }
    if (email.length > 100) {
        requirements.push('menos de 100 caracteres');
    }

    // Mostrar los requisitos si el correo electrónico no cumple con ellos
    if (requirements.length > 0) {
        emailRequirements.innerText = 'El correo electrónico debe tener ' + requirements.join(', ');
    } else {
        emailRequirements.innerText = '';
    }
});	


// Comprobar que ambas contraseñas son idénticas
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    // const passwordInputs = document.querySelectorAll('#new-password');
    const errorContainer = document.getElementById('password-error');

    form.addEventListener('submit', function (event) {
        
        if (passwordInputs[0].value !== passwordInputs[1].value) {
            event.preventDefault(); // Evita el envío del formulario
            errorContainer.innerText = 'Las contraseñas no coinciden';
        } 
        else {
            errorContainer.innerText = ''; // Elimina el mensaje de error
        }
    });
});
