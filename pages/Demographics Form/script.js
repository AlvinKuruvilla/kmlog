let keystrokeData = [];

function setup() {
  noCanvas();

  // Add event listeners for input fields
  document.getElementById("response1").addEventListener("keydown", logKeystroke);
  document.getElementById("response1").addEventListener("keyup", logKeystroke);
  document.getElementById("response2").addEventListener("keydown", logKeystroke);
  document.getElementById("response2").addEventListener("keyup", logKeystroke);

  // Add event listener for the submit button
  document.getElementById("submit").addEventListener("click", downloadData);
}

function logKeystroke(event) {
  const question = event.target.id === "response1" ? "Question 1" : "Question 2";
  const keyType = event.key;
  const keyEvent = event.type; // keydown or keyup
  const timestamp = Date.now(); // Unix timestamp

  keystrokeData.push({ question, keyType, keyEvent, timestamp });
}

function downloadData() {
  const jsonData = JSON.stringify(keystrokeData, null, 2);
  const blob = new Blob([jsonData], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "keystroke_data.json";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}