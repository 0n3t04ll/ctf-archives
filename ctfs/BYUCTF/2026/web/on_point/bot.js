var express = require("express");
var bodyParser = require("body-parser");
var puppeteer = require("puppeteer");
var app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

// endpoint to submit links to
app.post("/report", async function (req, res) {
    var url = req.body.url;
    var browser;
    try {
        browser = await puppeteer.launch({
            headless: "new",
            args: ["--no-sandbox", "--disable-setuid-sandbox"],
        });
        var page = await browser.newPage();
        await page.setCookie({
            name: "flag",
            value: "REDACTED",
            domain: "something",
            path: "/",
        });
        console.log("Visiting " + url);
        await page.goto(url, { waitUntil: "networkidle0", timeout: 10000 });
        await new Promise((r) => setTimeout(r, 3000));
    } catch (e) {
        console.log("Error visiting: " + e.message);
    } finally {
        if (browser) await browser.close();
    }
    res.sendFile(__dirname + "/public/response.html");
});

// main page to submit link
app.get("/", function (req, res) {
    res.sendFile(__dirname + "/public/index.html");
});

// start app
app.listen(1337, () => {
    console.log("Running on 1337");
});
