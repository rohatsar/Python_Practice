import socketio
import eventlet

sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print("Client connected:", sid)


@sio.event
def chat_message(sid, data):
    """
    Beklenen data:
    {
        "username": "Rohat",
        "message": "Hello"
    }
    """
    username = data.get("username", "Unknown")
    message = data.get("message", "")

    print(f"Message from {username}: {message}")

    # Broadcast edilecek metni hazırlıyoruz
    formatted = f"{username} says: {message}"

    # Tüm bağlı client'lara gönder (sender dahil)
    sio.emit("new_message", {"text": formatted})


@sio.event
def disconnect(sid):
    print("Client disconnected:", sid)


if __name__ == "__main__":
    print("Chat server is running on port 5000...")
    eventlet.wsgi.server(eventlet.listen(("", 5000)), app)
