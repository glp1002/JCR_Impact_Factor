const preview = document.querySelector('.imgperf');

preview.addEventListener('click', function() {
    if (this.classList.contains('active')){
        this.classList.toggle('active');
    }   
})



// Get the modal
var modal = document.getElementById("myModal");
                      
// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementById("myImg");
var modalImg = document.getElementById("imgperf");
var captionText = document.getElementById("caption");
img.onclick = function(){
  modal.style.display = "block";
  modalImg.src = this.src;
  captionText.innerHTML = this.alt;
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
  modal.style.display = "none";
}


// Cambio del botón de acceso a la lista de revistas
$(function () {
  $('#config-img').hover(
    function () {
      $(this).attr('src', '/static/images/config-hover.png');
    },
    function () {
      $(this).attr('src', '/static/images/config.png');
    }
  );
});
