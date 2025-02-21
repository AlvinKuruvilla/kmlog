let tweet_button = document.querySelector(".tweetBox__tweetButton");
tweet_button.addEventListener("click", async () => {
  console.log("Tweet button clicked!");
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
    alert("Response from Python server:", result);
    post.innerText = result.message; // Display the server response
  } catch (error) {
    console.log("Error:", error);
  }
});
