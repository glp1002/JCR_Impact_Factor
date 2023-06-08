var editTextImg = document.getElementById("edit-text");
var editPhotoImg = document.getElementById("small-image");
var newProfileImg = document.getElementById('profile-picture');
document.addEventListener('DOMContentLoaded', function () {
    // Cambio del botón de edición de texto
    editTextImg.addEventListener('mouseover', function () {
        editTextImg.src = '/static/images/edit_text_lil.png';
    });
    editTextImg.addEventListener('mouseout', function () {
        editTextImg.src = '/static/images/edit_text_bl.png';
    });

    // Cambio del botón de edición de imagen
    editPhotoImg.addEventListener('mouseover', function () {
        editPhotoImg.src = '/static/images/edit_photo_lil.png';
    });
    editPhotoImg.addEventListener('mouseout', function () {
        editPhotoImg.src = '/static/images/edit_photo_bl.png';
    });

    // Escuchar el evento 'change' del input de imagen
    editPhotoImg.addEventListener('click', function (event) {
        if (event.target.files && event.target.files[0]) {
            var file = event.target.files[0]; // Obtener el archivo seleccionado

            // Crear un objeto FileReader
            var reader = new FileReader();

            // Definir la función de callback cuando se complete la lectura del archivo
            reader.onload = function () {
                // Actualizar la imagen actual con la nueva imagen seleccionada
                newProfileImg.src = reader.result;
            };

            // Leer el archivo como una URL de datos (data URL)
            reader.readAsDataURL(file);
        }
    });
});

// Habilitar edición
var editionMode = true;
var nombreElement = document.getElementById("nombre");
var correoElement = document.getElementById("correo");
var saveChangesBtn = document.getElementById('save-changes');
var nombreOriginal = '';
var correoOriginal = '';

function habilitarEdicion() {
    if (editionMode === true) {
        // Guardar los valores originales
        nombreOriginal = nombreElement.innerHTML;
        correoOriginal = correoElement.innerHTML;

        // Convertir los elementos de texto en cajas de texto editables
        nombreElement.innerHTML = '<input type="text" name="nombre" value="' + nombreOriginal + '">';
        correoElement.innerHTML = '<input type="email" name="correo" value="' + correoOriginal + '">';
        saveChangesBtn.removeAttribute('hidden');
        editionMode = false;
    } else {
        // Restaurar los valores originales
        nombreElement.innerHTML = nombreOriginal;
        correoElement.innerHTML = correoOriginal;
        saveChangesBtn.setAttribute('hidden', true);
        editionMode = true;
    }
}

