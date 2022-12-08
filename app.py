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

class Person:
    name = []

    def set_name(self, user_name):
        self.name.append(user_name)
        return len(self.name) - 1

    def get_name(self, user_id):
        if user_id >= len(self.name):
            return 'There is no such user'
        else:
            return self.name[user_id]


if __name__ == '__main__':
    person = Person()
    print('User Abbas has been added with id ', person.set_name('Abbas'))
    print('User associated with id 0 is ', person.get_name(0))

# if __name__ == '__main__':
#     excel.init_excel(app)
#     app.run(host='0.0.0.0')