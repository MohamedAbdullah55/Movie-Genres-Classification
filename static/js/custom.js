form = document.getElementById("form")
submitBtn = document.getElementById("submitBtn")
form.onchange =  function(event){
    var preview = document.querySelector('.img-cont img');
    var file    = document.querySelector('input[type=file]').files[0];
    var reader  = new FileReader();


    reader.onloadend = function (e) {
        preview.src = reader.result;
    }

    if (file) {
        reader.readAsDataURL(file);
    } else {
        preview.src = "";
  }

  submitBtn.style.cursor = "pointer"
  submitBtn.removeAttribute("disabled")
}

form.onsubmit = function(e){
   loader = document.getElementsByClassName("loader")[0]
   loader.style.display = "unset"
}