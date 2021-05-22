/************************
Required External Modules
************************/
const express = require('express');
const path = require('path');
const {spawn} = require('child_process');
const glob = require('glob')
const fs = require('fs');

/************
App Variables 
************/
const app = express();
const port = process.env.PORT || "8000";
const http = require('http');
const server = http.createServer(app);

/*****************
Routes Definitions
*****************/
app.get('/', function(req, res) {
    res.render("index", { title: "Home" });
});

app.get('/update', function(req, res) {
    /* Spawn new child process to call the python script */
    req.setTimeout(0) // no timeout for all requests, your server will be DoS'd
    console.log("/update received")
    const python = spawn('python', ['webscraper.py']);
    var pythonData;

    /* Getting python script output */
    python.stdout.on('data', function(data) { 
        pythonData = data.toString().slice();
    });
    
    /* In close event we are sure that stream is from child process is closed */
    python.on('exit', (code) => {
        console.log("/update responded")
        if (pythonData != undefined) {
            pythonData = pythonData.slice(0, pythonData.length - 2);
            if (pythonData == "Error, no products were scanned") {
                code = -1;
            }
        }

        if (code == -1) {
            console.log(`Python process closed with code: ${code}, no products error!`);
            res.status(490).send("Error490");
        } else if (code != 0) {
            console.log(`Python process closed with code: ${code}, general error!`);
            res.status(491).send("Error491");
        } else {
            console.log(`Python process closed with code: ${code}, success!`);
            res.send("Success");
        }  
    });
});

app.get('/download', function(req, res) {
    console.log("/download received");
    const file = glob.sync(`${__dirname}/saved/*xlsx`).map(name => ({name, ctime: fs.statSync(name).ctime})).sort((a, b) => b.ctime - a.ctime)[0].name;
    console.log("/download responded");
    res.download(file);
});

/****************
Server Activation
****************/
server.listen(port, () => {
    console.log(`Listening to requests on http://localhost:${port}`);
});

/****************
App Configuration
****************/
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "pug");
app.use(express.static(path.join(__dirname, "public")));