const fs = require("fs");

const express = require("express");
let router = express.Router();
router.use(express.urlencoded());
router.use(express.json());

router.use("/css", express.static('public/css'));
router.use("/img", express.static('public/img'));

function updateData(file)
{
    var rawData = fs.readFileSync(__dirname + '/../datafiles/' + file);
    var data = JSON.parse(rawData);

    return data;
}

// Index pagina
router.get("/", laadIndex);

// Instellingen pagina
router.get("/instellingen", laadInstellingen);

// Permission Climbing Pagina
router.get("/permissionClimbing", laadPermissionClimbing);

// Regex Search Word Pagina
router.get("/regexSearchWords", laadRegexSearchWord);

// Regex Reactions Pagina
router.get("/regexReactions", laadRegexReactions);

// Regex Bans Pagina
router.get("/regexBans", laadRegexBans);

// DM Pagina
router.get("/DM", laadDMs);

// Custom Text Pagina
router.get("/customText", laadCustomText);

// Cogs Pagina
router.get("/cogs", laadCogs);

// =============================================================================================================

// Index pagina
function laadIndex(req, res)
{
    nav = updateData("pages.json");

    res.render("index", {page: "Home", "navId": "indexNav", "nav": nav});
}

// Instellingen pagina
function laadInstellingen(req, res)
{
    instellingen = updateData("botSettings.json");
    nav = updateData("pages.json");

    res.render("instellingen", {page: "Instellingen", "navId": "instellingenNav", "nav": nav, "instellingen": instellingen});
}

// Permission Climbing Pagina
function laadPermissionClimbing(req, res)
{
    config = updateData("permissionClimbing.json");
    nav = updateData("pages.json");

    res.render("permissionClimbing", {page: "Permission Climbing", "navId": "permissionClimbingNav", "nav": nav, "config": config});
}

// Regex Search Words Pagina
function laadRegexSearchWord(req, res)
{
    searchWords = updateData("regexSearchWords.json");
    nav = updateData("pages.json");

    res.render("regexSearchWords", {page: "Regex Search Words", "navId": "regexSearchWordsNav", "nav": nav, "data": searchWords});
}

// Regex Reactions Pagina
function laadRegexReactions(req, res)
{
    searchWords = updateData("regexReactions.json");
    nav = updateData("pages.json");

    res.render("regexReactions", {page: "Regex Reactions", "navId": "regexReactionsNav", "nav": nav, "data": searchWords});
}

// Regex Bans Pagina
function laadRegexBans(req, res)
{
    searchWords = updateData("regexBans.json");
    nav = updateData("pages.json");

    res.render("regexBans", {page: "Regex Bans", "navId": "regexBansNav", "nav": nav, "data": searchWords});
}

// DM Pagina
function laadDMs(req, res)
{
    DMlist = updateData("DMs.json");
    nav = updateData("pages.json");

    res.render("DMs", {page: "DMs", "navId": "DMNav", "nav": nav, "data": DMlist});
}

// Custom Text Pagina
function laadCustomText(req, res)
{
    text = updateData("customText.json");
    nav = updateData("pages.json");

    res.render("customText.ejs", {page: "Custom Text", "navId": "customTextNav", "nav": nav, "customText": text.text});
}

// Cogs Pagina
function laadCogs(req, res)
{
    data = updateData("cogs.json");
    nav = updateData("pages.json");

    res.render("cogs.ejs", {page: "Custom Text", "navId": "customTextNav", "nav": nav, "data": data});
}

module.exports = router;