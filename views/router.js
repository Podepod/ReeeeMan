const fs = require("fs");

const express = require("express");
let router = express.Router();
router.use(express.urlencoded());
router.use(express.json());

router.use("/css", express.static('public/css'));
router.use("/img", express.static('public/img'));




module.exports = router;

// Index pagina
router.get("/", laadIndex);


// Index pagina
function laadIndex(req, res)
{
    res.render("index", {page: "Home", "navId": "indexNav"});
}