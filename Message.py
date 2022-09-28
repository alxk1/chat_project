from datetime import datetime
from flask import session
import json


class Message:
    def __init__(self, msg):
        self.timestamp = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        self.user = session.get('username')
        self.msg = msg


class NotificationMessage(Message):
    def __init__(self, msg=None):
        super().__init__(msg)
