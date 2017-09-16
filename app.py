from flask import Flask, render_template
from flask_socketio import SocketIO, emit


# Create a flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# Use the flask app to create a socketio decorator
socketio = SocketIO(app)
thread = None


def background_thread():
    count = 0
    while True:
        socketio.sleep(2)
        count += 1
        """
            On every 2 seconds, the server send message to the client with updated count.
            First parameter of emit function tells which function to call on client side.
            So the following part of index.html will be called.

            socket.on('my_response', function(msg) {
                $('span#view').text(msg.count);
            });
            
        """
        socketio.emit('my_response',
                      {'data': 'Message from server', 'count': count},
                      namespace='/test')


@app.route('/')
def index():
    """
        Home page view function
    """
    return render_template('index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        # Once any client is connected, the background_thread function starts in loop
        thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5050)
