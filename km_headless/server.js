const express = require("express");
const cors = require("cors");
let current_user = null;
const app = express();
app.use(cors());
app.use(express.json());

app.post("/start-server", (req, res) => {
  console.log(req.body);
  let user_id = req.body.user_id;
  let platform_id = req.body.platform_id;
  current_user = { user_id, platform_id };

  console.log("Starting Keylogging service!");
  return res.status(200);
});
app.get("/get-current-user", (req, res) => {
  if (current_user) {
    return res.status(200).json(current_user);
  } else {
    return res.status(404).json({ message: "No active user" });
  }
});

app.listen(5500);
