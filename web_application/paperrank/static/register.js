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
        requirements.push(gettext('al menos 8 caracteres'));
    }
    if (!/\d/.test(password)) {
        requirements.push(gettext('al menos un número'));
    }
    if (!/[A-Z]/.test(password)) {
        requirements.push(gettext('al menos una letra mayúscula'));
    }

    // Mostrar los requisitos si la contraseña no cumple con ellos
    if (requirements.length > 0) {
        passwordRequirements.innerText = gettext('La contraseña debe contener: ') + requirements.join(', ');
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
        requirements.push(gettext('una dirección válida'));
    }
    if (email.length > 100) {
        requirements.push(gettext('menos de 100 caracteres'));
    }

    // Mostrar los requisitos si el correo electrónico no cumple con ellos
    if (requirements.length > 0) {
        emailRequirements.innerText = gettext('El correo electrónico debe tener ') + requirements.join(', ');
    } else {
        emailRequirements.innerText = '';
    }
});
  

// Control del submit
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const usernameInput = document.getElementById('new-username');
    const emailInput = document.getElementById('new-email');
    const passwordInputs = document.querySelectorAll('#new-password');
    const usernameError = document.getElementById('username-error');
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');
  
    // Variables de confirmación
    let isUsernameValid = true;
    let isEmailValid = true;
    let isPasswordValid = true;
  
    // Función para validar el nombre de usuario
    const validateUsername = () => {
      const username = usernameInput.value;
      if (username) {
        fetch(`/validateUser/${username}`)
          .then(response => response.json())
          .then(result => {
            if (result) {
                usernameError.textContent = '';
                isUsernameValid = true;
            } else {
                // El nombre de usuario ya existe
                var texto = gettext("El nombre de usuario ya está en uso");
                usernameError.textContent = texto;
                isUsernameValid = false;
              
            }
          })
          .catch(error => {
            console.error('Error al validar el nombre de usuario:', error);
            isUsernameValid = false;
          });
      } else {
        usernameError.textContent = '';
        isUsernameValid = false;
      }
    };
  
    // Función para validar el correo electrónico
    const validateEmail = () => {
      const email = emailInput.value;
      if (email) {
        fetch(`/validateEmail/${email}`)
          .then(response => response.json())
          .then(result => {
            if (result) {
                emailError.textContent = '';
                isEmailValid = true;
            } else {
                // El correo electrónico ya existe
                emailError.textContent = gettext('El correo electrónico ya está en uso');
                isEmailValid = false;
            }
          })
          .catch(error => {
            console.error('Error al validar el correo electrónico:', error);
            isEmailValid = false;
          });
      } else {
        emailError.textContent = '';
        isEmailValid = false;
      }
    };
  
    // Agregar eventos blur a los campos de nombre de usuario y correo electrónico
    usernameInput.addEventListener('blur', validateUsername);
    emailInput.addEventListener('blur', validateEmail);
  
    // Función para validar el formulario antes del envío
    const validateForm = (event) => {
      const usernameErrorText = usernameError.textContent;
      const emailErrorText = emailError.textContent;
  
      if (usernameErrorText || emailErrorText) {
        // Si hay mensajes de error, evita el envío del formulario
        event.preventDefault();
      }
  
      if (passwordInputs[0].value !== passwordInputs[1].value) {
        event.preventDefault(); // Evita el envío del formulario
        passwordError.textContent = gettext('Las contraseñas no coinciden');
        isPasswordValid = false;
      } else {
        passwordError.textContent = ''; // Elimina el mensaje de error
        isPasswordValid = true;
      }
  
      // Comprobar todas las validaciones
      if (isUsernameValid && isEmailValid && isPasswordValid) {
        const confirmation = confirm(gettext("Su registro se ha realizado correctamente"));
        if (!confirmation) {
          event.preventDefault(); // Evita el envío del formulario si se cancela la confirmación
        }
      }
    };
  
    // Agrega el evento de envío al formulario
    form.addEventListener('submit', validateForm);
  });
  