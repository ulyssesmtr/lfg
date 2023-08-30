const express = require('express')
const app = express()
const PORT = 3000
const HOST = '0.0.0.0';


app.listen(PORT, HOST, () => {
    console.log(`Running on http://${HOST}:${PORT}`);
  });
  
app.get('/', (req, res) => {
     res.sendFile(__dirname + "/static/index.html");
})

app.use(express.static(__dirname + "/static"));

