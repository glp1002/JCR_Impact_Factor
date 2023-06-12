var editTextImg = document.getElementById("edit-text");
var editPhotoImg = document.getElementById("small-image");
var newProfileImg = document.getElementById('profile-picture');
var selectFileBtn = document.getElementById('select-file-btn');
var fileInput = document.getElementById('file-input');
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

    const dropArea = document.getElementById('drop-area');
    let dropAreaVisible = false; // Variable para controlar la visibilidad del drop area
    // Escuchar el evento 'click' del input de imagen
    editPhotoImg.addEventListener('click', () => {
        if (dropAreaVisible) {
            selectFileBtn.style.display = 'none';
            dropArea.style.display = 'none'; // Ocultar el drop area si ya está visible
            dropAreaVisible = false;
        } else {
            selectFileBtn.style.display = 'block';
            dropArea.style.display = 'block'; // Mostrar el drop area si está oculto
            dropAreaVisible = true;
        }
    });


    // Evitar que el navegador abra la imagen al arrastrar y soltar
    dropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
    });


    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();

        const file = e.dataTransfer.files[0];
        const fileReader = new FileReader();

        fileReader.onload = () => {
            const imgDataUrl = fileReader.result;

            // Crear un objeto FormData para enviar la imagen al endpoint en Flask
            const formData = new FormData();
            formData.append('image', file);

            // Realizar una solicitud POST al endpoint en Flask
            fetch('/insert_profile_picture', {
                method: 'POST',
                body: formData
            })
                .then(response => {
                    if (response.ok) {
                        console.log('La imagen se ha guardado exitosamente');
                        // Recargar la página sin usar la caché del navegador
                        location.reload();
                    } else {
                        console.error('Error al guardar la imagen');
                    }
                })
                .catch(error => {
                    console.error('Error en la solicitud:', error);
                });
        };

        fileReader.readAsDataURL(file);
    });



    selectFileBtn.addEventListener('click', function () {
        fileInput.click(); // Simular un clic en el input de archivo
    });

    fileInput.addEventListener('change', function (e) {
        const file = e.target.files[0];
        const fileReader = new FileReader();

        fileReader.onload = function () {
            const imgDataUrl = fileReader.result;

            // Crear un objeto FormData para enviar la imagen al endpoint en Flask
            const formData = new FormData();
            formData.append('image', file);

            // Realizar una solicitud POST al endpoint en Flask
            fetch('/insert_profile_picture', {
                method: 'POST',
                body: formData
            })
                .then(response => {
                    if (response.ok) {
                        console.log('La imagen se ha guardado exitosamente');
                        // Recargar la página sin usar la caché del navegador
                        location.reload();

                    } else {
                        console.error('Error al guardar la imagen');
                    }
                })
                .catch(error => {
                    console.error('Error en la solicitud:', error);
                });
        };

        fileReader.readAsDataURL(file);
    });


    var url = "/get_profile_picture";
    // Obtener foto de perfil del usuario haciendo un GET
    fetch(url)
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                throw new Error("No se pudo obtener la imagen");
            }
        })
        .then(blob => {
            var imageUrl = URL.createObjectURL(blob);
            $("#profile-picture").attr("src", imageUrl);
        })
        .catch(error => {
            console.log("Error al obtener la imagen:", error);
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

$(document).ready(function () {
    var url = "/get_profile_picture";

    fetch(url)
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                throw new Error("No se pudo obtener la imagen");
            }
        })
        .then(blob => {
            var imageUrl = URL.createObjectURL(blob);
            $("#profile-picture").attr("src", imageUrl);
        })
        .catch(error => {
            console.log("Error al obtener la imagen:", error);
        });
});

