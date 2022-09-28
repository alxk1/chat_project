from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit

from Message import Message, NotificationMessage
from flask_session import Session

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)
app.secret_key = "my_secret_key"

default_room = "main_room"

message_history = []


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if (session.get('username') is not None):
        return render_template('chat.html', session=session)

    if ('txtName' in request.form):
        session['username'] = request.form['txtName']
        return render_template('chat.html', session=session)

    return redirect(url_for('index'))


@socketio.on('join_chat_call', namespace='/chat')
def join(_):
    join_room(default_room)
    emit('new_member_notification', NotificationMessage().__dict__, room=default_room)


@socketio.on('message_call', namespace='/chat')
def message_sent(message):
    emit('message_sent', Message(message['msg']).__dict__, room=default_room)


@socketio.on('leave_chat_call', namespace='/chat')
def leave_chat(message):
    msg = NotificationMessage().__dict__
    leave_room(default_room)
    session.clear()
    emit('member_leave_notification', msg, room=default_room)


if __name__ == '__main__':
    app.run()
