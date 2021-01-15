console.log('Client-side code running');

const updateButton = document.getElementById('update');
updateButton.addEventListener('click', function(e) {
  updateButton.innerHTML = "Updating List...";
  updateButton.disabled = true;
  updateButton.style = "background-color: #e65449; cursor: auto !important;"
  var req = new XMLHttpRequest();
  req.open("GET","/update");
  req.onreadystatechange = function(){
    if(req.readyState == 4) {
      updateButton.innerHTML = "Update Laptop List"
      updateButton.disabled = false;
      updateButton.style = "background-color: #3091db;"
      location.reload();
    }
  }
  req.send();
  console.log('Update button was clicked');
});