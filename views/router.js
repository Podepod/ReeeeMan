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

// Custom Text Pagina
router.get("/customText", laadCustomText);

// =============================================================================================================

// Index pagina
function laadIndex(req, res)
{
    pages = updateData("pages.json");

    res.render("index", {page: "Home", "navId": "indexNav", "data": pages});
}

// Instellingen pagina
function laadInstellingen(req, res)
{
    instellingen = updateData("botSettings.json");

    res.render("instellingen", {page: "Instellingen", "navId": "instellingenNav", "instellingen": instellingen});
}

// Permission Climbing Pagina
function laadPermissionClimbing(req, res)
{
    config = updateData("permissionClimbing.json");

    res.render("permissionClimbing", {page: "Permission Climbing", "navId": "permissionClimbingNav", "config": config});
}

// Regex Search Words Pagina
function laadRegexSearchWord(req, res)
{
    searchWords = updateData("regexSearchWords.json");

    res.render("regexSearchWords", {page: "Regex Search Words", "navId": "regexSearchWordsNav", "data": searchWords});
}

// Regex Reactions Pagina
function laadRegexReactions(req, res)
{
    searchWords = updateData("regexReactions.json");

    res.render("regexReactions", {page: "Regex Reactions", "navId": "regexReactionsNav", "data": searchWords});
}

// Regex Bans Pagina
function laadRegexBans(req, res)
{
    searchWords = updateData("regexBans.json");

    res.render("regexBans", {page: "Regex Bans", "navId": "regexBansNav", "data": searchWords});
}

// Custom Text Pagina
function laadCustomText(req, res)
{
    text = updateData("customText.json");

    res.render("customText.ejs", {page: "Custom Text", "navId": "customTextNav", "customText": text.text});
}

module.exports = router;