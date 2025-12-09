import socketio
import eventlet

sio = socketio.Server()
app = socketio.WSGIApp(sio)

# chat namespace

@sio.on("connect", namespace="/chat")
def connect_chat(sid, environ):
    print("Client connected to /chat:", sid)


@sio.on("disconnect", namespace="/chat")
def disconnect_chat(sid):
    print("Client disconnected from /chat:", sid)


@sio.on("chat_message", namespace="/chat")
def handle_chat_message(sid, data):
    # data: {"username": "Rohat", "message": "Hello"}
    username = data.get("username", "Unknown")
    message = data.get("message", "")

    print(f"[CHAT] {username}: {message}")

    formatted = f"{username}: {message}"
    # /chat namespace'ine bağlı tüm client'lara mesajı gönder
    sio.emit("chat_message", {"text": formatted}, namespace="/chat")


# status namespace

@sio.on("connect", namespace="/status")
def connect_status(sid, environ):
    print("Client connected to /status:", sid)


@sio.on("disconnect", namespace="/status")
def disconnect_status(sid):
    print("Client disconnected from /status:", sid)


@sio.on("health_check", namespace="/status")
def health_check(sid):
    print("Health check requested")
    # Client callback ile bu değeri alacak
    return "ok"




if __name__ == "__main__":
    print("Namespace server is running on port 5000...")
    eventlet.wsgi.server(eventlet.listen(("", 5000)), app)
