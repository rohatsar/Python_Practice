import socketio

# Socket.IO client nesnesi
sio = socketio.Client()


@sio.event
def connect():
    print("Connected to server")


@sio.on("welcome")
def handle_welcome(data):
    # Sunucudan gelen mesajı yazdır
    print("Server says:", data.get("message", ""))


@sio.event
def disconnect():
    print("Disconnected from server")


if __name__ == "__main__":
    sio.connect("http://localhost:5000")
    # Bağlı kalması için
    sio.wait()