console.log('Client-side code running');

const updateButton = document.getElementById('update');
updateButton.addEventListener('click', function(e) {
  var req = new XMLHttpRequest();
  req.open("GET","/update");
  req.onreadystatechange = function(){
    if(req.readyState == 4){
      location.reload();
    }
  }
  req.send();
  console.log('Update button was clicked');
});