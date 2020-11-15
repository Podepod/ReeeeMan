const express = require("express");
const fs = require('fs');
let api = express.Router();
api.use(express.urlencoded());
api.use(express.json());

function updateData(file)
{
    var rawData = fs.readFileSync('/home/pi/Discord/ReeeeMan/datafiles/' + file);
    var data = JSON.parse(rawData);

    return data;
}

function changeData(file, data)
{
    var schrijfData = JSON.stringify(data, null, 2);
    fs.writeFile('/home/pi/Discord/ReeeeMan/datafiles/' + file, schrijfData, writeFileFinished);
}

api.get("/bot/settings", getSettings);
api.get("/bot/customText", getCustomText);
api.post("/bot/customText", changeCustomText);

function getSettings(req, res)
{
    settingsData = updateData("botSettings.json");

    reply = {
        status: "success",
        data: settingsData
    }

    res.send(reply);
}

function getCustomText(req, res)
{
    customTextData = updateData("customText.json");

    reply = {
        status: "success",
        data: customTextData
    }

    res.send(reply);
}

function changeCustomText(req, res)
{
    customTextData = updateData("customText.json");

    newText = req.body.newText;

    customTextData.text = newText;

    changeData("customText.json", customTextData);

    if (req.body.redirect){
        res.redirect(req.body.redirect);
    } else{
        var reply = {
            status: "succes",
            data: customTextData.text
        }
        res.send(reply);
    }
}

module.exports = api;