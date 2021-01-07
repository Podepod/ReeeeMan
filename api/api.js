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
api.get("/bot/regexReactions", getRegexReactionData);
api.post("/bot/regexReactions/:action", changeRegexReactionData);
api.get("/bot/regexBans", getRegexBanData);
api.post("/bot/regexBans/:action", changeRegexBanData);
api.get("/bot/DM", getDMData);
api.post("/bot/DM/:action", changeDMData);
api.get("/bot/cogs/list", getCogData);
api.post("/bot/cogs/:action", changeCogData);
api.get("/bot/vibes/:action", getVibesData);
api.get("/bot/vibes/:action", changeVibesData);

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

    settingsData["log"]["channelID"] = req.body.log.channelID;

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

    customTextData.text = req.body.newText;

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

function getRegexReactionData(req, res)
{
    regexReactionData = updateData("regexReactions.json");

    reply = {
        status: "success",
        data: regexReactionData
    };

    res.send(reply);
}

function changeRegexReactionData(req, res)
{
    regexReactionData = updateData("regexReactions.json");

    wordIndex = 0;

    if (req.params.action == "edit")
    {
        wordIndex = Number(req.body.index);
        regexReactionData[req.body.index].regex = req.body.regex;
        regexReactionData[req.body.index].reaction = req.body.reaction;
        regexReactionData[req.body.index].enabled = (req.body.enabled == "true");
    } 
    else if (req.params.action == "add")
    {
        tempData = {
            "regex": req.body.regex,
            "reaction": req.body.reaction,
            "enabled": (req.body.enabled == "true"),
            "userOnly": false,
            "userID": ""
        };

        regexReactionData.push(tempData);
    }
    else if (req.params.action == "remove")
    {        
        regexReactionData.splice(Number(req.body.index), 1);
    }

    changeData("regexReactions.json", regexReactionData);

    if(req.body.redirect)
    {
        res.redirect(req.body.redirect);
    }
    else
    {
        var reply = {
            status: "succes",
            data: regexReactionData[wordIndex]
        };
        res.send(reply);
    }
}

function getRegexBanData(req, res)
{
    regexBanData = updateData("regexBans.json");

    reply = {
        status: "success",
        data: regexBanData
    };

    res.send(reply);
}

function changeRegexBanData(req, res)
{
    regexBanData = updateData("regexBans.json");

    wordIndex = 0;

    if (req.params.action == "edit")
    {
        wordIndex = Number(req.body.index);
        regexBanData[req.body.index].regex = req.body.regex;
        regexBanData[req.body.index].ownerAnswer = req.body.ownerAnswer;
        regexBanData[req.body.index].answer = req.body.answer;
        regexBanData[req.body.index].enabled = (req.body.enabled == "true");
    } 
    else if (req.params.action == "add")
    {
        tempData = {
            "regex": req.body.regex,
            "ownerAnswer": req.body.ownerAnswer,
            "answer": req.body.answer,
            "enabled": (req.body.enabled == "true"),
            "userOnly": false,
            "userID": ""
        };

        regexBanData.push(tempData);
    }
    else if (req.params.action == "remove")
    {        
        regexBanData.splice(Number(req.body.index), 1);
    }

    changeData("regexBans.json", regexBanData);

    if(req.body.redirect)
    {
        res.redirect(req.body.redirect);
    }
    else
    {
        var reply = {
            status: "succes",
            data: regexBanData[wordIndex]
        };
        res.send(reply);
    }
}

function getDMData(req, res)
{
    DMData = updateData("DMs.json");

    reply = {
        status: "success",
        data: DMData
    };

    res.send(reply);
}

function changeDMData(req, res)
{
    DMData = updateData("DMs.json");

    wordIndex = 0;

    if (req.params.action == "edit")
    {
        wordIndex = Number(req.body.index);
        DMData[req.body.index].link = req.body.link;
        DMData[req.body.index].text = req.body.text;
        DMData[req.body.index].enabled = (req.body.enabled == "true");
    } 
    else if (req.params.action == "add")
    {
        tempData = {
            "link": req.body.link,
            "text": req.body.text,
            "enabled": (req.body.enabled == "true"),
        };

        DMData.push(tempData);
    }
    else if (req.params.action == "remove")
    {        
        DMData.splice(Number(req.body.index), 1);
    }

    changeData("DMs.json", DMData);

    if(req.body.redirect)
    {
        res.redirect(req.body.redirect);
    }
    else
    {
        var reply = {
            status: "succes",
            data: DMData[wordIndex]
        };
        res.send(reply);
    }
}

function getCogData(req, res){
    cogData = updateData("cogs.json");

    reply = {
        status: "success",
        data: cogData
    };

    res.send(reply);
}

function changeCogData(req, res){
    cogData = updateData("cogs.json");
    if (req.params.action == "change")
    {
        cogIndex = 0;

        cogIndex = Number(req.body.index);
        if (req.body.action == "load"){
            cogData[cogIndex].enabled = true;
        }
        else if (req.body.action == "unload"){
            cogData[cogIndex].enabled = false;
        }
        else{
            cogData[cogIndex].enabled = (req.body.enabled == "true");
        }
        if(req.body.name){
            cogData[cogIndex].name = req.body.name
        }
    }
    else if(req.params.action == "add")
    {
        tempData = {
            "name": req.body.name,
            "enabled": (req.body.enabled == "true"),
        };

        cogData.push(tempData);
    }
    else if(req.params.action == "remove")
    {
        cogData.splice(Number(req.body.index), 1);
    }

    changeData("cogs.json", cogData);

    if(req.body.redirect)
    {
        res.redirect(req.body.redirect);
    }
    else
    {
        var reply = {
            status: "succes",
            data: cogData[cogIndex]
        };
        res.send(reply);
    }
}

function getVibesData(req, res){
    vibes = updateData("vibes.json");

    if(req.params.action == "random"){
        vibeTypes = ["positive", "negative", "neutral", "neither"];
        randomNumber = Math.floor(Math.random() * 4);
        vibeType = vibeTypes[randomNumber];
        vibeTypeLen = vibes[vibeType].length;
        ReplyData = vibes[vibeType][Math.floor(Math.random() * vibeTypeLen)];
        replyStatus = "Success";
    }
    else if (req.params.action == "all"){
        replyData = vibes;
        replyStatus = "Success";
    }
    else{
        replyData = "Action not found.";
        replyStatus = "Failed";
    }

    reply = {
        status: replyStatus,
        data: replyData
    };

    res.send(reply);
}

function changeVibesData(req, res){
    res.send("not working yet... :/");
}

module.exports = api;