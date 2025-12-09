import socketio
import eventlet

sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print("Client connected:", sid)


@sio.event
def login(sid, data):
    """
    Beklenen data:
    {
        "username": "Rohat",
        "level": 5
    }
    """
    username = data.get("username", "Guest")
    level = data.get("level", 0)

    print(f"Login request from {username}, level: {level}")

    message = f"Hello {username}! Your level is {level}."
    # Sadece bu client'a cevap gönder
    sio.emit("login_response", {"message": message}, to=sid)


@sio.event
def disconnect(sid):
    print("Client disconnected:", sid)


if __name__ == "__main__":
    print("Server is running on port 5000...")
    eventlet.wsgi.server(eventlet.listen(("", 5000)), app)
