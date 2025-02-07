let tweet_button = document.querySelector(".tweetBox__tweetButton")
tweet_button.addEventListener('click', async () =>{
    console.log("Tweet button clicked!");
    try {
        const response = await fetch('http://127.0.0.1:5000/end-server', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        console.log(response);
        if (!response.ok) {
            const errorData = await response.json();
            alert('Failed to send special request:', errorData);
            return;
        }

        const result = await response.json();
        alert('Response from Python server:', result);
        post.innerText = result.message; // Display the server response
    } catch (error) {
        console.log('Error:', error);
    }

});
window.onload = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/start-server', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            // Twitter's platform id = 2
            body: JSON.stringify({ platform_id: 2  }),
        });

        console.log(response);
        if (!response.ok) {
            alert('Failed to send special request: ' + response.status);
            return;
        }

        const result = await response.json();
        alert('Response from Python server: ' + result.message);
        post.innerText = result.message; // Display the server response
    } catch (error) {
        console.log('Error:', error);
    }
};