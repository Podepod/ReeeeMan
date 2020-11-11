#!/usr/bin/nodejs
const express = require('express');
const fs = require('fs');
const morgan = require('morgan');

const app = express();
const api = require('/home/pi/Discord/ReeeeMan/api/api');
//const router = require('/home/pi/Discord/ReeeeMan/views/routes');
const port = 4005;

//app.set('view engine', 'ejs');
//app.set('views', '/home/pi/Discord/ReeeeMan/views');

app.use(morgan('common', 
  {stream: fs.createWriteStream('/home/pi/Discord/ReeeeMan/logs/weblog.log', {flags: 'a'})
}));

//app.use("/", router);

app.use("/api", api);

//app.use("/javascript", express.static(__dirname + '/views/javascript'));

app.listen(port, err => {
  if(err){
    return console.log("ERROR:", err);
  }
});