async function send() {
  try {
    const response = await fetch("http://127.0.0.1:5000/start-server", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      // Facebook's platform id = 0
      body: JSON.stringify({ platform_id: 0 }),
    });

    console.log(response);
    if (!response.ok) {
      alert("Failed to send special request: " + response.status);
      return;
    }

    const result = await response.json();
    alert("Response from Python server: " + result.message);
  } catch (error) {
    console.log("Error:", error);
  }
}
await send();