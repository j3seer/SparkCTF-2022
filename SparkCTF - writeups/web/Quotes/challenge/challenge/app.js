
const express = require('express');
const app = express();
const router = express.Router();
const bodyparser = require("body-parser");
const fs = require('fs');
var bot = require('./admin.js');


app.use(bodyparser())
app.use('/public', express.static('public'))
app.use('/', router);
app.set("view engine", "ejs");



app.use(function (req, res, next) {
    res.setHeader(
      'Content-Security-Policy', "script-src https://cdn.jsdelivr.net/ 'unsafe-eval';connect-src 'self';object-src 'none' ;style-src 'self'  https://cdnjs.cloudflare.com https://unicons.iconscout.com;"
   );
   next();
  });


app.get('/', function(req, res) {
    res.render("index")
});

app.post('/report',function(req,res){
   const url = req.body.url_submitted

   var expression = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
   var regex = new RegExp(expression);
   
   if (url.match(regex)) {
        try{
            bot.visitUrl(url);
            res.render("admin",{
                visit_status:`Thanks for submitting a bug!<br>The admin has visited the URL `
            });
        }catch(error){    
            res.render("admin",{
                visit_status:`Something went wrong.. `
            });
                console.log(error)
        }
   }else{
        res.render("admin",{
            visit_status:`You didn't suppply a valid URL!`
        });
   }
});

app.get('/search', function(req, res) {

    const q = req.query.q

    if (q == ''){
        return res.render("search",{
            query:"You didn't supply something to search for...",
            result :''
        });
    }

    result = []

    let file = fs.readFileSync("Quotes.txt", "utf8");
    let arr = file.split(/\r?\n/);
    arr.forEach((line, idx)=> {
        if(line.includes(q)){
            result.push(line)
        }
    });

    if (result.length === 0) {
        result = ["Not found"]
    }

    res.render("search",{
        query:'Seach results for \''+q+'\' :',
        results:result
    });

});

// error stuff

app.use(function(err, req, res, next) {
    res.status(500);
    console.log(err)
    res.render("error", {
        error: "Idk what you did..but an error has occurred..."
    })
});

app.use(function(err, req, res, next) {});

app.listen(5252)