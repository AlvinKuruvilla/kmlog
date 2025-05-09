var settingsMenu = document.querySelector(".setting_menu");
var darkBtn = document.getElementById("dark_btn");

function settingsMenuToggle() {
  settingsMenu.classList.toggle("setting_menu_height");
}
function getQueryParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

/**
 * Start recording keystrokes and expose a “Submit Keylog” button.
 * The button uploads a CSV (keystrokes) and a TXT (raw text typed in
 * the #input_value element) to the Netlify `saver` function.
 */
function startKeyLogger(user_id_str, platform_initial, task_id) {
  /* -------------------- 1.  collect events -------------------- */
  const keyEvents = [];

  const onKeyDown = (e) => keyEvents.push(["P", e.key, Date.now()]);
  const onKeyUp = (e) => keyEvents.push(["R", e.key, Date.now()]);

  document.addEventListener("keydown", onKeyDown);
  document.addEventListener("keyup", onKeyUp);

  /* -------------------- 2.  helper to upload a file ------------ */
  const uploadToSaver = async (fileBlob, filename) => {
    const fd = new FormData();
    fd.append("file", fileBlob, filename);

    const res = await fetch(
      "https://melodious-squirrel-b0930c.netlify.app/.netlify/functions/saver",
      { method: "POST", body: fd }
    );

    const json = await res.json();
    if (!res.ok) throw new Error(json?.error || res.statusText);
    return json.url; // public URL returned by your function
  };

  /* -------------------- 4.  click handler ---------------------- */
  btnGet.onclick = async () => {
    if (btnGet.disabled) return; // avoid double‑clicks
    btnGet.disabled = true;

    try {
      /* ---- filenames ---- */
      const p =
        platform_initial === "0"
          ? "f"
          : platform_initial === "1"
          ? "i"
          : platform_initial === "2"
          ? "t"
          : "u";
      const csvName = `${p}_${user_id_str}_${task_id}.csv`;
      const txtName = `${p}_${user_id_str}_${task_id}_raw.txt`;

      /* ---- build CSV ---- */
      const heading = [["Press or Release", "Key", "Time"]];
      const csvString = heading
        .concat(keyEvents)
        .map((row) => row.join(","))
        .join("\n");
      const csvBlob = new Blob([csvString], {
        type: "text/csv;charset=utf-8",
      });

      /* ---- build TXT ---- */
      const inputEl = document.getElementById("input_value");
      const rawText = inputEl ? inputEl.value : ""; // safe if element missing
      if ((!rawText || rawText.length === 0) && keyEvents.length === 0) {
        alert("Non-empty posts are not allowed!");
      } else {
        console.error(rawText);
        const txtBlob = new Blob([rawText], {
          type: "text/plain;charset=utf-8",
        });

        /* ---- upload both in parallel ---- */
        const [csvUrl, txtUrl] = await Promise.all([
          uploadToSaver(csvBlob, csvName),
          uploadToSaver(txtBlob, txtName),
        ]);

        console.log("✅ CSV uploaded →", csvUrl);
        console.log("✅ TXT uploaded →", txtUrl);
        console.log("✅ Keylog submitted!");
        alert(
          "Keystroke CSV and raw text uploaded successfully! Close this tab and begin the next task!"
        );
      }
      /* ---- optional: stop recording after successful upload ---- */
      // document.removeEventListener("keydown", onKeyDown);
      // document.removeEventListener("keyup",   onKeyUp);
    } catch (err) {
      console.error("❌ Upload failed:", err);
      console.error("❌ Upload failed – see console for details");
      btnGet.disabled = false; // let user try again
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
