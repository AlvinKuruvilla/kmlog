let tweet_button = document.querySelector(".tweetBox__tweetButton");
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
  tweet_button.onclick = async () => {
    if (tweet_button.disabled) return; // avoid double‑clicks
    tweet_button.disabled = true;

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
      if (!rawText || rawText.length === 0) {
        alert("Empty posts are not allowed!");
        tweet_button.disabled = false; // Re-enable button so the user can try again
      } else if (rawText.length < 200) {
        alert("posts shorter than 200 chars are not allowed!");
        tweet_button.disabled = false; // Re-enable button so the user can try again
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
          "Keystroke CSV and raw text uploaded successfully! This tab will be closed after dismissing this message!"
        );
        window.close();
      }
      /* ---- optional: stop recording after successful upload ---- */
      // document.removeEventListener("keydown", onKeyDown);
      // document.removeEventListener("keyup",   onKeyUp);
    } catch (err) {
      console.error("❌ Upload failed:", err);
      console.error("❌ Upload failed – see console for details");
      tweet_button.disabled = false; // let user try again
    }
  };
}

function getQueryParam(name) {
  return new URLSearchParams(window.location.search).get(name);
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
