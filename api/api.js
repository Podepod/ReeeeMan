const express = require("express");
let api = express.Router();
api.use(express.urlencoded());
api.use(express.json());

function updateData(file)
{
    var rawData = fs.readFileSync('/home/pi/Discord/ReeeeMan/datafiles/' + file);
    var data = JSON.parse(rawData);

    return data;
}

api.get("/bot/customText", getCustomText);

function getCustomText(req, res)
{
    customTextData = updateData("customText.json");

    reply = {
        status: "success",
        data: customTextData
    }

    res.send(reply);
}

module.exports = api;