
jQuery(document).ready(function() {
    /* Check if the files exist on the server, which determines which buttons should start as ghosted or not */
    function checkFilesFunc() { 
        $.ajax({
            type: 'get',
            url: '/checkforfiles',
            dataType: 'json',
    
            success: function(data) {
                if(data["LastUpdated"] != "") {
                    const timeStatus = document.getElementById('time');
                    timeStatus.innerHTML = "Data Last Updated: " + data["LastUpdated"]
                }
                
                console.log("Call to '/checkforfiles' succeeded");
            },
            error: function(error) {
                console.log("Call to '/checkforfiles' failed (" + error.status + ")");
            }
        });
    }
    const sec = 1000;
    console.log('Client-side code running');
    checkFilesFunc();
    
    /* Update the list of information on the website */
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
                    checkFilesFunc()
                    console.log("Call to '/update' succeeded");
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
                console.log("Call to '/update' failed (" + error.status + ")");
            }
        });
    });

    /* Download the general excel spreadsheet */
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
            console.log("Call to '/download' succeeded");
        },
        error: function(error) {
            downloadButton.innerHTML = "Download Latest Sheet"
            downloadButton.disabled = false;
            downloadButton.style = "background-color: #3091db;"
            console.log("Call to '/download' failed (" + error.status + ")");
        }
        });
    });
});