import socketio
import eventlet

sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print("Client connected:", sid)


@sio.event
def join_room(sid, data):
    """
    Beklenen data:
    {
        "room": "roomA",
        "username": "Rohat"
    }
    """
    room = data.get("room")
    username = data.get("username", "Unknown")

    if room not in ["roomA", "roomB"]:
        print(f"{username} tried to join invalid room:", room)
        return

    sio.enter_room(sid, room)
    print(f"{username} joined {room}")

    # Odaya bilgi mesajı gönder
    sio.emit(
        "room_info",
        {"text": f"{username} joined {room}."},
        room=room
    )


@sio.event
def room_message(sid, data):
    """
    Beklenen data:
    {
        "room": "roomA",
        "username": "Rohat",
        "message": "Hello"
    }
    """
    room = data.get("room")
    username = data.get("username", "Unknown")
    message = data.get("message", "")

    if room not in ["roomA", "roomB"]:
        print(f"Message to invalid room from {username}:", room)
        return

    print(f"[{room}] {username}: {message}")

    formatted = f"[{room}] {username}: {message}"

    # Sadece belirtilen odadaki kullanıcılara yayın
    sio.emit("room_message", {"text": formatted}, room=room)


@sio.event
def disconnect(sid):
    print("Client disconnected:", sid)


if __name__ == "__main__":
    print("Room server is running on port 5000...")
    eventlet.wsgi.server(eventlet.listen(("", 5000)), app)
