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

// =============================================================================================================

// Index pagina
function laadIndex(req, res)
{
    res.render("index", {page: "Home", "navId": "indexNav"});
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

module.exports = router;