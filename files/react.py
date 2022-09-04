index_html = """<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE-edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title></title>
    </head>

    <body>
        <div id="root"></div>
        <script src="main.js"></script>
    </body>
</html>
"""

babelrc = """{
  "presets": [
    "@babel/preset-env",
    "@babel/preset-react"
  ],
  "plugins": [
    "@babel/plugin-transform-runtime"
  ]
}
"""

webpack_config_js = """const path = require("path");

module.exports = {
  mode: "development",
  entry: "src/index.js",
  output: {
    path: path.resolve(__dirname, "public"),
    filename: "main.js",
  },

  target: "web",
  devServer: {
    port: "3000",
    static: ["./public"],
    open: true,
    hot: true,
    liveReload: true,
  },
  resolve: {
    extensions: [".js", ".jsx", ".json", ".ts"]
  },
  module: {
    rules: [
        {
            test: /\.(js|jsx)$/,
            exclude: /node_modules/,
            use: "babel-loader",
        }
    ]
  }
}
"""

App = """import React from "react";

const App = () => {
    return (
        <div>
            Hello, World!
        </div>
    );
};

export default App;
"""

index_js="""import React from "react";
import ReactDOM from "react-dom";
import App from "./App";

ReactDOM.render(<App />, document.querySelector("#root"));
"""

server = """const express = require("express");
const app = express();
const path = require("path");
const port = process.env.PORT || 3000;

app.listen(port, () => {
   console.log(`The app server is running on port: ${port}`);
});

const DIST_DIR = path.join(__dirname, "dist");
const HTML_FILE = path.join(DIST_DIR, "index.html");

app.use(express.json());
app.use(express.static("public"));
app.use(express.static("dist"));

app.get("/", (req, res) => {
   res.sendFile(HTML_FILE, function(err){
      if(err){
         res.status(500).send(err);
      }
   });
});
"""
