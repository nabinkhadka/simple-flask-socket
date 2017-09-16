from flask import Flask, render_template
from flask_socketio import SocketIO, emit

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None


def background_thread():
    count = 0
    while True:
        socketio.sleep(2)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Message from server', 'count': count},
                      namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5050)
