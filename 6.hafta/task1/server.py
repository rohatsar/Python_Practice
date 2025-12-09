import socketio
import eventlet

# Socket.IO server nesnesi
sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print("Client connected:", sid)
    # Bağlanan client'a hoş geldin mesajı gönder
    sio.emit("welcome", {"message": "Welcome to the Socket.IO server!"}, to=sid)


@sio.event
def disconnect(sid):
    print("Client disconnected:", sid)


if __name__ == "__main__":
    print("Server is running on port 5000...")
    eventlet.wsgi.server(eventlet.listen(("", 5000)), app)
