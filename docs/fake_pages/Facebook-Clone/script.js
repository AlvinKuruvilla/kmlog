var settingsMenu = document.querySelector(".setting_menu");
var darkBtn = document.getElementById("dark_btn");

function settingsMenuToggle() {
  settingsMenu.classList.toggle("setting_menu_height");
}
function getQueryParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

function startKeyLogger(user_id_str, platform_initial, task_id) {
  const keyEvents = [];

  document.addEventListener("keydown", (e) =>
    keyEvents.push(["P", e.key, Date.now()])
  );
  document.addEventListener("keyup", (e) =>
    keyEvents.push(["R", e.key, Date.now()])
  );

  const button = document.createElement("button");
  button.textContent = "Submit Keylog";
  button.style.position = "fixed";
  button.style.bottom = "10px";
  button.style.right = "10px";
  button.style.background = "black";
  button.style.color = "white";
  document.body.appendChild(button);

  // --- click handler ---------------------------------------------------------
  button.onclick = async () => {
    /* 1 — build filename ----------------------------------------------------- */
    const platform_letter =
      platform_initial === "0"
        ? "f"
        : platform_initial === "1"
        ? "i"
        : platform_initial === "2"
        ? "t"
        : "u"; // u = unknown / fallback
    const filename = `${platform_letter}_${user_id_str}_${task_id}.csv`;

    /* 2 — build CSV blob ----------------------------------------------------- */
    const heading = [["Press or Release", "Key", "Time"]];
    const csvString = heading
      .concat(keyEvents)
      .map((row) => row.join(","))
      .join("\n");
    const blob = new Blob([csvString], {
      type: "text/csv;charset=utf-8",
    });

    /* 3 — send to Netlify Function ------------------------------------------ */
    const formData = new FormData();
    formData.append("file", blob, filename); // filename → Content‑Disposition

    try {
      const res = await fetch(
        "https://melodious-squirrel-b0930c.netlify.app/.netlify/functions/saver",
        {
          method: "POST",
          body: formData, // fetch sets the correct multipart boundary
        }
      );
      const result = await res.json();

      if (res.ok && result.url) {
        console.log("✅ Uploaded!", result.url);
        console.log(`✅ Uploaded!\nURL: ${result.url}`);
      } else {
        console.error("❌ Upload failed:", result);
      }
    } catch (err) {
      console.error("❌ Network/function error:", err);
      alert("❌ Could not reach serverless function");
    }
    const typed_text_blob = new Blob(
      [document.getElementById("input_value").value],
      {
        type: "text/plain;charset=utf-8",
      }
    );
    const typed_text_form_data = new FormData();
    const raw_text_filename = `${platform_letter}_${user_id_str}_${task_id}_raw.txt`;

    typed_text_form_data.append("file", typed_text_blob, raw_text_filename);
    try {
      const res = await fetch(
        "https://melodious-squirrel-b0930c.netlify.app/.netlify/functions/saver",
        {
          method: "POST",
          body: typed_text_form_data, // fetch sets the correct multipart boundary
        }
      );
      const result = await res.json();

      if (res.ok && result.url) {
        console.log("✅ Uploaded!", result.url);
        console.log(`✅ Uploaded!\nURL: ${result.url}`);
      } else {
        console.error("❌ Upload failed:", result);
      }
    } catch (err) {
      console.error("❌ Network/function error:", err);
      alert("❌ Could not reach serverless function to send raw data");
    }
  };
}
window.onload = async function () {
  const user_id = getQueryParam("user_id");
  const platform_id = getQueryParam("platform_id");
  const task_id = getQueryParam("task_id");

  if (user_id && platform_id && task_id) {
    startKeyLogger(user_id, platform_id, task_id);
  } else {
    alert("Missing user or platform or task info in URL");
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
      // alert("Failed to send special request:", errorData);
      return;
    }

    const result = await response.json();
    // alert("Response from Python server:", result);
    post.innerText = result.message; // Display the server response
  } catch (error) {
    console.log("Error:", error);
  }
};
