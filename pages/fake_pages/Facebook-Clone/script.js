var settingsMenu = document.querySelector(".setting_menu");
var darkBtn = document.getElementById("dark_btn");

function settingsMenuToggle() {
  settingsMenu.classList.toggle("setting_menu_height");
}
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
  event.preventDefault()
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
