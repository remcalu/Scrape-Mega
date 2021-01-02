/************************
Required External Modules
************************/
const express = require('express');
const path = require('path');
const http = require('http');
const {spawn} = require('child_process');

/************
App Variables 
************/
const app = express();
const port = process.env.PORT || "8000";

/*****************
Routes Definitions
*****************/
// Default URL for website
app.get("/", (req, res) => {
    res.render("index", { title: "Home" });
});

app.get('/', function(req, res) {
 
    var dataToSend;

    // Spawn new child process to call the python script
    const python = spawn('python', ['webscraper.py']);

    // Collect data from script
    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();
    });

    // In close event we are sure that stream from child process is closed
    python.on('close', function(code) {
        console.log(`child process close all stdio with code ${code}`);

        // Send data to browser
        res.send(dataToSend)
    });

});

/****************
Server Activation
****************/
app.listen(port, () => {
    console.log(`Listening to requests on http://localhost:${port}`);
});

/****************
App Configuration
****************/
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "pug");
app.use(express.static(path.join(__dirname, "public")));