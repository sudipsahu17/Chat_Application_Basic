from ChatApplication import create_app, create_socket

app = create_app()
socketio = create_socket(app)

if __name__ == '__main__':
    #app.run()
    socketio.run(app)
