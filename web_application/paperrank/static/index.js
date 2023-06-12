const preview = document.querySelector('.imgperf');
// Dropdown de la imagen de perfil
preview.addEventListener('click', function () {
  if (this.classList.contains('active')) {
    this.classList.toggle('active');
  }
})



// Get the modal
var modal = document.getElementById("myModal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementById("myImg");
var modalImg = document.getElementById("imgperf");
var captionText = document.getElementById("caption");
img.onclick = function () {
  modal.style.display = "block";
  modalImg.style.height = "70%";
  modalImg.style.width = "auto";
  modalImg.src = this.src;
  captionText.innerHTML = this.alt;
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = "none";
}


// Cambio del botón de acceso al cambio de idioma
var languageImg = document.getElementById("config-img");
languageImg.addEventListener('mouseover', function () {
  languageImg.src = '/static/images/lang-hover.png';
});
languageImg.addEventListener('mouseout', function () {
  languageImg.src = '/static/images/lang.png';
});


// Obtener imagen de perfil
$(document).ready(function() {
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
      $("#myImg").attr("src", imageUrl);
    })
    .catch(error => {
      console.log("Error al obtener la imagen:", error);
    });
});

