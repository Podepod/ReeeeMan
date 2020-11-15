#!/usr/bin/nodejs
const express = require('express');
const fs = require('fs');
const morgan = require('morgan');

const app = express();
const api = require(__dirname + '/api/api');
const router = require(__dirname + '/views/router');
const port = 4005;

app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');

app.use(morgan('common', 
  {stream: fs.createWriteStream(__dirname + '/logs/weblog.log', {flags: 'a'})
}));

app.use("/", router);

app.use("/api", api);

app.use("/public", express.static(__dirname + '/public'));

app.listen(port, err => {
  if(err){
    return console.log("ERROR:", err);
  }
});