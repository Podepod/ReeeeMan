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
api.get("/bot/searchWordData", getSearchWordData);
api.post("/bot/searchWordData/:action", changeSearchWordData);

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
    permissionClimbingData["make_new_role"]["color"] = req.body.make_new_role.color;
    permissionClimbingData["make_new_role"]["hoist"] = (req.body.make_new_role.hoist == "true");
 
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

function getSearchWordData(req, res)
{
    searchWordData = updateData("regexSearchWords.json");

    reply = {
        status: "success",
        data: searchWordData
    };

    res.send(reply);
}

function changeSearchWordData(req, res)
{
    searchWordData = updateData("regexSearchWords.json");

    wordIndex = 0;

    if (req.params.action == "edit")
    {
        wordIndex = req.body.index;
        searchWordData[req.body.index].regex = req.body.regex;
        searchWordData[req.body.index].response = req.body.response;
        searchWordData[req.body.index].tts = (req.body.tts == "true");
        searchWordData[req.body.index].enabled = (req.body.enabled == "true");
        searchWordData[req.body.index].removeMessage = (req.body.removeMessage == "true");
    } 
    else if (req.params.action == "add")
    {
        tempData = {
            "regex": req.body.regex,
            "response": req.body.response,
            "tts": (req.body.tts == "true"),
            "enabled": (req.body.enabled == "true"),
            "removeMessage": (req.body.removeMessage == "true")
        };

        searchWordData.push(tempData);
    }
    else if (req.params.action == "remove")
    {        
        searchWordData.splice(Number(req.body.index), 1);
    }

    changeData("regexSearchWords.json", searchWordData);

    if(req.body.redirect)
    {
        res.redirect(req.body.redirect);
    }
    else
    {
        var reply = {
            status: "succes",
            data: searchWordData[wordIndex]
        };
        res.send(reply);
    }
}

module.exports = api;