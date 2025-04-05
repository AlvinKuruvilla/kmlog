var settingsMenu = document.querySelector(".setting_menu");
var darkBtn = document.getElementById("dark_btn");

function settingsMenuToggle() {
  settingsMenu.classList.toggle("setting_menu_height");
}
function getQueryParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

function startKeyLogger(user_id_str, platform_initial) {
  const keyEvents = [];

  document.addEventListener("keydown", function (event) {
    keyEvents.push(["P", event.key, Date.now()]);
    console.log(`Pressed: ${event.key}`);
  });

  document.addEventListener("keyup", function (event) {
    keyEvents.push(["R", event.key, Date.now()]);
    console.log(`Released: ${event.key}`);
  });
  const button = document.createElement("button");
  button.textContent = "Download Keylog";
  button.style.position = "fixed";
  button.style.bottom = "10px";
  button.style.right = "10px";
  button.style.background = "black";
  button.style.color = "white";
  button.onclick = () => {
    let platform_letter = null;
    if (platform_initial == "0") {
      platform_letter = "f";
    } else if (platform_initial == "1") {
      platform_letter = "i";
    } else if (platform_initial == "2") {
      platform_letter = "t";
    }
    const filename = `${platform_letter}_${user_id_str}.csv`;
    const heading = [["Press or Release", "Key", "Time"]];
    const final_events = heading.concat(keyEvents);
    console.error(final_events);
    const csvString = final_events.map((row) => row.join(",")).join("\n");
    const blob = new Blob([csvString], { type: "text/csv;charset=utf-8;" });

    if (navigator.msSaveBlob) {
      // IE 10+
      navigator.msSaveBlob(blob, filename);
    } else {
      const link = document.createElement("a");
      if (link.download !== undefined) {
        // Browsers that support HTML5 download attribute
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", filename);
        link.style.visibility = "hidden";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    }
  };
  document.body.appendChild(button);
}
window.onload = async function () {
  const user_id = getQueryParam("user_id");
  const platform_id = getQueryParam("platform_id");

  if (user_id && platform_id) {
    startKeyLogger(user_id, platform_id);
  } else {
    alert("Missing user or platform info in URL");
  }
};
darkBtn.onclick = function () {
  darkBtn.classList.toggle("dark_btn_on");
};
function passvalue() {
  var message = document.getElementById("");
}

let btnGet = document.querySelector("#button_value");
let inputGet = document.querySelector("#input_vlaue");
let post = document.querySelector("#post");

btnGet.onclick = async function (event) {
  event.preventDefault();
  try {
    const response = await fetch("http://127.0.0.1:5000/end-server", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log(response);
    if (!response.ok) {
      const errorData = await response.json();
      alert("Failed to send special request:", errorData);
      return;
    }

    const result = await response.json();
    // alert("Response from Python server:", result);
    post.innerText = result.message; // Display the server response
  } catch (error) {
    console.log("Error:", error);
  }
};
