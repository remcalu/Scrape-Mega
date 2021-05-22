jQuery(document).ready(function() {
  const sec = 1000;
  console.log('Client-side code running');

  $('#update').on('click', function(e) {
    const updateButton = document.getElementById('update');
    updateButton.innerHTML = "Updating List...";
    updateButton.disabled = true;
    updateButton.style = "background-color: #e65449; cursor: auto !important;"

    $.ajax({
      type: 'get',
      url: '/update',

      success: function(data) {
        setTimeout(function() { 
          updateButton.innerHTML = "Update Laptop List"
          updateButton.disabled = false;
          updateButton.style = "background-color: #3091db;"
          console.log('S: Update button was clicked');
        }, sec * 300);
      },
      error: function(error) {
        updateButton.innerHTML = "Error, Try again later"
        updateButton.disabled = true;
        updateButton.style = "background-color: #FFAD00; cursor: auto !important;"
        setTimeout(function() { 
          updateButton.innerHTML = "Update Laptop List"
          updateButton.disabled = false;
          updateButton.style = "background-color: #3091db;"
        }, sec * 5);
        console.log('F: Update button was clicked (' + error.status + ')');
      }
    });
  });

  $('#download').on('click', function(e) {
    const downloadButton = document.getElementById('download');
    downloadButton.innerHTML = "Downloaded Sheet!";
    downloadButton.disabled = true;
    downloadButton.style = "background-color: #3dbd2f; cursor: auto !important;"

    $.ajax({
      type: 'get',
      url: '/download',

      success: function(data) {
        setTimeout(function() { 
          downloadButton.innerHTML = "Download Latest Sheet"
          downloadButton.disabled = false;
          downloadButton.style = "background-color: #3091db;"
        }, sec * 5);
        console.log('S: Download button was clicked');
      },
      error: function(error) {
        downloadButton.innerHTML = "Download Latest Sheet"
        downloadButton.disabled = false;
        downloadButton.style = "background-color: #3091db;"
        console.log('F: Download button was clicked (' + error.status + ')');
      }
    });
  });
});