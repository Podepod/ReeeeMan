const express = require("express");
const fs = require('fs');
let api = express.Router();
api.use(express.urlencoded());
api.use(express.json());

function updateData(file)
{
    var rawData = fs.readFileSync(__dirname + '/../datafiles/' + file);
    var data = JSON.parse(rawData);

    return data;
}

function changeData(file, data)
{
    var schrijfData = JSON.stringify(data, null, 2);
    fs.writeFile(__dirname + '/../datafiles/' + file, schrijfData, writeFileFinished);
}

function writeFileFinished(err)
{
    if(err)
    {
        console.log(err);
    }
}

api.get("/bot/settings", getSettings);
api.post("/bot/settings", changeSettings);
api.get("/bot/customText", getCustomText);
api.post("/bot/customText", changeCustomText);
api.get("/bot/permissionClimbing", getPermissionClimbing);
api.post("/bot/permissionClimbing", changePermissionClimbing);

function getSettings(req, res)
{
    settingsData = updateData("botSettings.json");

    reply = {
        status: "success",
        data: settingsData
    };

    res.send(reply);
}

function changeSettings(req, res)
{
    settingsData = updateData("botSettings.json");

    settingsData["basic"]["token"] = req.body.basic.token;
    settingsData["basic"]["prefix"] = req.body.basic.prefix;
    settingsData["basic"]["name"] = req.body.basic.name;
    settingsData["basic"]["description"] = req.body.basic.description;
    settingsData["basic"]["version"] = req.body.basic.version;

    settingsData["activity"]["status"] = req.body.activity.status;
    settingsData["activity"]["text"] = req.body.activity.text;
    settingsData["activity"]["link"] = req.body.activity.link;
    settingsData["activity"]["activity"] = req.body.activity.activity;

    changeData("botSettings.json", settingsData);

    if(req.body.redirect)
    {
        res.redirect(req.body.redirect);
    }
    else
    {
        var reply = {
            status: "succes",
            data: settingsData
        };
        res.send(reply);
    }
}

function getCustomText(req, res)
{
    customTextData = updateData("customText.json");

    reply = {
        status: "success",
        data: customTextData
    };

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
        };
        res.send(reply);
    }
}

function getPermissionClimbing(req, res)
{
    permissionClimbingData = updateData("permissionClimbing.json");

    reply = {
        status: "success",
        data: permissionClimbingData
    };

    res.send(reply);
}

function changePermissionClimbing(req, res)
{
    permissionClimbingData = updateData("permissionClimbing.json");

    permissionClimbingData["enabled"] = (req.body.enabled == "true");

    permissionClimbingData["log"]["enabled"] = (req.body.log.enabled == "true");
    permissionClimbingData["log"]["channel"] = req.body.log.channel;

    permissionClimbingData["make_new_role"]["enabled"] = (req.body.make_new_role.enabled == "true");
    permissionClimbingData["make_new_role"]["name"] = req.body.make_new_role.name;
 
    changeData("permissionClimbing.json", permissionClimbingData);

    if(req.body.redirect)
    {
        res.redirect(req.body.redirect);
    }
    else
    {
        var reply = {
            status: "succes",
            data: permissionClimbingData
        };
        res.send(reply);
    }
}

module.exports = api;