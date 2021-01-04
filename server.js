/************************
Required External Modules
************************/
const express = require('express');
const path = require('path');
const {spawn} = require('child_process');
const glob = require('glob')
const fs = require('fs'); //File System

/************
App Variables 
************/
const app = express();
const port = process.env.PORT || "8000";

/*****************
Routes Definitions
*****************/
app.get('/', function(req, res) {
    res.render("index", { title: "Home" });
});

app.get('/update', function(req, res) {
    // Spawn new child process to call the python script
    const python = spawn('python', ['webscraper.py']);
    
    // For debugging python script
    python.stdout.on('data', function(data) { 
        console.log(data.toString()); 
    }); 

    // In close event we are sure that stream is from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // Send data to browser
        res.send("Done")
    });
});

app.get('/download', function(req, res){
    const file = glob.sync(`${__dirname}/saved/*xlsx`).map(name => ({name, ctime: fs.statSync(name).ctime})).sort((a, b) => b.ctime - a.ctime)[0].name
    res.download(file); // Set disposition and send it.
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