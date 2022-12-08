import DTree
import json
# import sys
import pprint as pp
from flask import Flask, jsonify, request, send_file
# from flask_socketio import SocketIO, emit
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from threading import Thread
import logging
import threading
import time
import ipaddress as ip
import uuid
import sys
import socket
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(10**6)
print(sys.getrecursionlimit())

flask_thread = []
flask_process_data = {}
flask_process = {}
import_obj_instance_hash = {}
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World! From ' + socket.gethostname()

@app.route('/process_data')
def process_data():
    return jsonify(flask_process_data), 200

def do_process(flask_data, json_file, import_obj_instance):
    if '.json' in json_file:
        c = DTree.DTree(json.load(open(json_file)), name=json_file,
                        import_obj_instance=import_obj_instance, data=flask_data)
    else:
        c = DTree.DTree(json_file, name=uuid.uuid1(),
                        import_obj_instance=import_obj_instance, data=flask_data)

@app.route('/start/<hash>', methods=['GET', 'POST'])
def start(hash):
    # name = names[hash]
    name = hash
    d = {}
    if request.method == 'POST':
        data = request.get_json()
        print('data: ', data)
        if 'jobs' in data:
            name = data.pop('jobs')
        d = data
    print('d: ', d)
    if hash in flask_process_data:
        flask_process_data[hash].update(d)
        import_obj_instance = import_obj_instance_hash[hash]

    else:
        print('NEW HASH: ', hash)
        flask_process_data[hash] = d
        import_obj_instance_hash[hash] = {}
        import_obj_instance = import_obj_instance_hash[hash]

    d = flask_process_data[hash]
    thread = threading.Thread(
        target=do_process, args=(d, name, import_obj_instance,))
    flask_process[hash] = thread
    thread.daemon = False
    thread.start()
    thread.join()

    d['uuid'] = hash

    return jsonify(d), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')